from typing import List, Optional
from src.match import Match
from src.competitor import Competitor
import math

class SingleElimination:
    def __init__(self, competitors: list[str] | list[Competitor]) -> None:
        self.competitors: List[Competitor] = [c if isinstance(c, Competitor) else Competitor(c) for c in competitors]
        self.rounds: List[List[Match]] = []
        self.current_round: int = 0
        self.generate_bracket()

    def generate_bracket(self) -> None:
        if len(self.competitors) < 2:
            return
        next_power_of_2 = 2 ** math.ceil(math.log2(len(self.competitors)))
        while len(self.competitors) < next_power_of_2:
            self.competitors.append(Competitor("TBD"))
        self.rounds.append([Match(self.competitors[i], self.competitors[i + 1])
                            for i in range(0, len(self.competitors), 2)])

    def get_current_round_matches(self) -> List[Match]:
        return self.rounds[self.current_round]

    def advance_to_next_round(self) -> Optional[List[Match]]:
        current_matches = self.get_current_round_matches()
        # Only keep actual winners (no None)
        winners = [winner for match in current_matches if (winner := match.get_winner()) is not None]
        if len(winners) < 2:
            return None
        next_round_matches: List[Match] = [
            Match(winners[i], winners[i + 1])
            for i in range(0, len(winners), 2)
        ]
        self.rounds.append(next_round_matches)
        self.current_round += 1
        return next_round_matches

    def is_tournament_over(self) -> bool:
        return len(self.rounds[-1]) == 1 and self.rounds[-1][0].get_winner() is not None

    def get_champion(self) -> Optional[Competitor]:
        if self.is_tournament_over():
            return self.rounds[-1][0].get_winner()
        return None