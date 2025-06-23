from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from src.competitor import Competitor

class Match:
    def __init__(self, competitor_a: "Competitor", competitor_b: "Competitor") -> None:
        self.competitor_a: "Competitor" = competitor_a
        self.competitor_b: "Competitor" = competitor_b
        self.winner = None

    def set_winner(self, winner: "Competitor") -> None:
        """Set the winner of the match."""
        if winner not in [self.competitor_a, self.competitor_b]:
            raise ValueError("Winner must be one of the competitors")
        self.winner = winner

    def get_winner(self) -> Optional["Competitor"]:
        """Get the winner of the match."""
        return self.winner
    
    def get_loser(self):
        """Get the loser of the match."""
        if self.winner is None:
            return None
        return self.competitor_b if self.winner == self.competitor_a else self.competitor_a