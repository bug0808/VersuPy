from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from src.competitor import Competitor

class Match:
    """Represents a match between two competitors."""
    def __init__(self, competitor_a: "Competitor", competitor_b: "Competitor") -> None:
        """
        Initialize a match.

        Args:
            competitor_a: The first competitor.
            competitor_b: The second competitor.
        """
        self.competitor_a: "Competitor" = competitor_a
        self.competitor_b: "Competitor" = competitor_b
        self.winner = None

    def set_winner(self, winner: "Competitor") -> None:
        """
        Set the winner of the match.

        Args:
            winner: The competitor who won the match.

        Raises:
            ValueError: If winner is not one of the competitors.
        """
        if winner not in [self.competitor_a, self.competitor_b]:
            raise ValueError("Winner must be one of the competitors")
        self.winner = winner

    def get_winner(self) -> Optional["Competitor"]:
        """Return the winner of the match, or None if not decided."""
        return self.winner
    
    def get_loser(self):
        """Return the loser of the match, or None if not decided."""
        if self.winner is None:
            return None
        return self.competitor_b if self.winner == self.competitor_a else self.competitor_a