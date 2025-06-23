class Competitor:
    """
    Represents a competitor in a tournament.
    """
    def __init__(self, name: str, wins: int = 0) -> None:
        """
        Initialize a competitor.

        Args:
            name: The name of the competitor.
            wins: The number of wins (default is 0).
        """
        self.wins = wins
        self.name = name
        self.has_bye = False
        self.buchholz_score = 0
        self.matches = []

