class Match:
    def __init__(self, competitor_a, competitor_b):
        self.competitor_a = competitor_a
        self.competitor_b = competitor_b
        self.winner = None

    def set_winner(self, winner):
        """Set the winner of the match."""
        if winner not in [self.competitor_a, self.competitor_b]:
            raise ValueError("Winner must be one of the competitors")
        self.winner = winner

    def get_winner(self):
        """Get the winner of the match."""
        return self.winner