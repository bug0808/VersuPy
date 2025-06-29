from typing import List, Optional
from versupy.match import Match
from versupy.competitor import Competitor

class RoundRobin:
    """
    Round robin tournament implementation.
    """
    def __init__(self, competitors: List[Competitor]) -> None:
        """
        Initialize a round robin tournament.

        Args:
            competitors: List of Competitor objects.
        """
        self.competitors: List[Competitor] = competitors
        self.matches: List[Match] = [Match(a, b) for i, a in enumerate(competitors) for b in competitors[i+1:]]
        self.current_match_index: int = 0
        self.results: List[tuple[Competitor, Competitor, Optional[Competitor]]] = []

    def get_current_round_matches(self) -> List[Match]:
        """
        Get matches for the current round.

        Returns:
            List of Match objects for the current round.
        """
        return self.matches[self.current_match_index:self.current_match_index + len(self.competitors) // 2]

    def advance_to_next_round(self) -> Optional[List[Match]]:
        """
        Advance to the next round and record results from the previous round.

        Returns:
            List of Match objects for the next round, or None if the tournament is over.
        """
        current_matches = self.get_current_round_matches()
        # Record results for the current round before advancing
        for match in current_matches:
            if match.get_winner() is not None:
                self.results.append((match.competitor_a, match.competitor_b, match.get_winner()))
        self.current_match_index += len(self.competitors) // 2
        if self.is_tournament_over():
            return None
        return self.get_current_round_matches()

    def is_tournament_over(self) -> bool:
        """
        Check if the tournament has concluded.

        Returns:
            True if the tournament is over, False otherwise.
        """
        return self.current_match_index >= len(self.matches)

    def get_champion(self) -> Optional[Competitor]:
        """
        Return the champion if the tournament is over.

        Returns:
            The winning Competitor, or None if the tournament is not over.
        """
        if not self.is_tournament_over():
            return None
        return max(self.competitors, key=lambda c: getattr(c, "wins", 0), default=None)