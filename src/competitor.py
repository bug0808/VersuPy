class Competitor:
    def __init__(self, name: str, wins: int = 0) -> None:
        self.wins = wins
        self.name = name
        self.has_bye = False
        self.buchholz_score = 0
        self.matches = []

