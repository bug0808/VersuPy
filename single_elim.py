from .match import Match
from .competitor import Competitor
import math

class SingleElimination:
    def __init__(self, competitors):
        self.competitors = [Competitor(name) for name in competitors]
        self.rounds = []
        self.current_round = 0
        self.generate_bracket()

    def generate_bracket(self):
        """Create the single elimination bracket."""
        next_power_of_2 = 2 ** math.ceil(math.log2(len(self.competitors)))
        while len(self.competitors) < next_power_of_2:
            self.competitors.append(Competitor("TBD"))

        self.rounds.append([Match(self.competitors[i], self.competitors[i + 1]) 
                            for i in range(0, len(self.competitors), 2)])

    def get_current_round_matches(self):
        return self.rounds[self.current_round]

    def advance_to_next_round(self):
        """Advance based on winners."""
        current_matches = self.get_current_round_matches()
        winners = [match.get_winner() for match in current_matches if match.get_winner()]

        if len(winners) < 2:
            return None  

        next_round_matches = [Match(winners[i], winners[i + 1]) 
                              for i in range(0, len(winners), 2)]
        self.rounds.append(next_round_matches)
        self.current_round += 1
        return next_round_matches

    def is_tournament_over(self):
        return len(self.rounds[-1]) == 1 and self.rounds[-1][0].get_winner() is not None
