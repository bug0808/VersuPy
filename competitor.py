class Competitor:
    def __init__(self, name, wins=0):
        self.wins = wins
        self.name = name
        self.has_bye = False
        self.buchholz_score = 0
        self.matches = []

