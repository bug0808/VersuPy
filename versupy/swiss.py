from typing import List, Optional, Dict, Union
from versupy.match import Match
from versupy.competitor import Competitor

class Swiss:
    @property
    def rounds(self) -> list:
        """Expose rounds in a similar way to other tournament types."""
        return self.matches

    def get_current_round_matches(self) -> List[Match]:
        """Return the matches for the current round (last generated round)."""
        if not self.matches:
            # Generate the first round if not already generated
            return self.generate_round_pairings()
        return self.matches[-1]

    def get_results(self) -> List[tuple[Competitor, Competitor, Optional[Competitor]]]:
        """Return all match results as (a, b, winner) tuples."""
        return self.results.copy()
    """
    Swiss-system tournament implementation.
    """
    def __init__(self, competitors: Union[List[str], List[Competitor]], rounds: Optional[int] = None) -> None:
        """
        Initialize a Swiss-system tournament.

        Args:
            competitors: List of competitor names or Competitor objects.
            rounds: Number of rounds to play (default: number of competitors - 1).
        """
        self.competitors: List[Competitor] = [Competitor(name) if isinstance(name, str) else name for name in competitors]
        for c in self.competitors:
            if not hasattr(c, "matches"):
                c.matches = []
        self.round: int = 1
        self.rounds_played: int = 0
        self.max_rounds: int = rounds if rounds else len(competitors) - 1
        self.matches: List[List[Match]] = []
        self._all_competitors: List[Competitor] = list(self.competitors)
        self.results: List[tuple[Competitor, Competitor, Optional[Competitor]]] = []
        

    def generate_round(self) -> List[Match]:
        """
        Generate pairings for the next round.

        Returns:
            List of Match objects for the round.
        """
        round_matches: List[Match] = self.generate_round_pairings()
        self.round += 1
        return round_matches

    def generate_round_pairings(self) -> List[Match]:
        """
        Pair competitors with similar win records for the next round.

        Returns:
            List of Match objects for the round.
        """
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
        """
        Record the results for the current round and update the results log.

        Args:
            results: List of winning Competitor objects for the current round.
        """
        for match, winner in zip(self.matches[-1], results):
            match.set_winner(winner)
            winner.wins += 1
            self.results.append((match.competitor_a, match.competitor_b, winner))
        

    def calculate_buchholz_scores(self) -> Dict[str, int]:
        """
        Calculate the Buchholz score for each competitor.

        Returns:
            Dictionary mapping competitor names to their Buchholz scores.
        """
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
        """
        Advance to the next round if possible.
        """
        if self.rounds_played < self.max_rounds:
            self.generate_round_pairings()
            self.rounds_played += 1
        

    def get_standings(self) -> List[Competitor]:
        """
        Return competitors sorted by their final standings, considering Buchholz if necessary.

        Returns:
            List of Competitor objects sorted by standings.
        """
        self.calculate_buchholz_scores()
        return sorted(self._all_competitors, key=lambda c: (c.wins, getattr(c, "buchholz_score", 0)), reverse=True)

    def is_tournament_over(self) -> bool:
        """
        Check if the tournament has concluded.

        Returns:
            True if the tournament is over, False otherwise.
        """
        return self.rounds_played >= self.max_rounds