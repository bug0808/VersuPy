from typing import List, Optional
from src.match import Match
from src.competitor import Competitor

class RoundRobin:
    def __init__(self, competitors: List[Competitor]) -> None:
        self.competitors: List[Competitor] = competitors
        self.matches: List[Match] = [Match(a, b) for i, a in enumerate(competitors) for b in competitors[i+1:]]
        self.current_match_index: int = 0

    def get_current_round_matches(self) -> List[Match]:
        return self.matches[self.current_match_index:self.current_match_index + len(self.competitors) // 2]

    def advance_to_next_round(self) -> Optional[List[Match]]:
        self.current_match_index += len(self.competitors) // 2
        if self.is_tournament_over():
            return None
        return self.get_current_round_matches()

    def is_tournament_over(self) -> bool:
        return self.current_match_index >= len(self.matches)

    def get_champion(self) -> Optional[Competitor]:
        if not self.is_tournament_over():
            return None
        return max(self.competitors, key=lambda c: getattr(c, "wins", 0), default=None)