from typing import List, Optional, Dict, Union
from src.match import Match
from src.competitor import Competitor

class Swiss:
    def __init__(self, competitors: Union[List[str], List[Competitor]], rounds: Optional[int] = None) -> None:
        self.competitors: List[Competitor] = [Competitor(name) if isinstance(name, str) else name for name in competitors]
        for c in self.competitors:
            if not hasattr(c, "matches"):
                c.matches = []
        self.round: int = 1
        self.rounds_played: int = 0
        self.max_rounds: int = rounds if rounds else len(competitors) - 1
        self.matches: List[List[Match]] = []
        self._all_competitors: List[Competitor] = list(self.competitors)

    def generate_round(self) -> List[Match]:
        round_matches: List[Match] = self.generate_round_pairings()
        self.round += 1
        return round_matches

    def generate_round_pairings(self) -> List[Match]:
        competitors: List[Competitor] = sorted(self.competitors, key=lambda c: c.wins, reverse=True)
        new_matches: List[Match] = []

        if len(competitors) % 2 == 1:
            for competitor in reversed(competitors):
                if not getattr(competitor, "has_bye", False):
                    competitor.wins += 1
                    competitor.has_bye = True
                    competitors.remove(competitor)
                    break

        while len(competitors) > 1:
            a, b = competitors.pop(0), competitors.pop(0)
            match = Match(a, b)
            new_matches.append(match)
            if not hasattr(a, "matches"):
                a.matches = []
            if not hasattr(b, "matches"):
                b.matches = []
            a.matches.append(match)
            b.matches.append(match)

        self.matches.append(new_matches)
        return new_matches

    def record_match_results(self, results: List[Competitor]) -> None:
        for match, winner in zip(self.matches[-1], results):
            match.set_winner(winner)
            winner.wins += 1

    def calculate_buchholz_scores(self) -> Dict[str, int]:
        buchholz_scores: Dict[str, int] = {}
        for competitor in self._all_competitors:
            score: int = 0
            for match in getattr(competitor, "matches", []):
                opponent = match.competitor_a if match.competitor_b == competitor else match.competitor_b
                score += getattr(opponent, "wins", 0)
            buchholz_scores[competitor.name] = score
            competitor.buchholz_score = score
        return buchholz_scores

    def advance_round(self) -> None:
        if self.rounds_played < self.max_rounds:
            self.generate_round_pairings()
            self.rounds_played += 1

    def get_standings(self) -> List[Competitor]:
        self.calculate_buchholz_scores()
        return sorted(self._all_competitors, key=lambda c: (c.wins, getattr(c, "buchholz_score", 0)), reverse=True)

    def is_tournament_over(self) -> bool:
        return self.rounds_played >= self.max_rounds