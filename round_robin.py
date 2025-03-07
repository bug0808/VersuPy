from .match import Match

class RoundRobin:
    def __init__(self, competitors):
        self.competitors = competitors
        self.matches = [Match(a, b) for i, a in enumerate(competitors) for b in competitors[i+1:]]
        self.current_match_index = 0

    def get_current_round_matches(self):
        return self.matches[self.current_match_index:self.current_match_index + len(self.competitors) // 2]

    def advance_to_next_round(self):
        self.current_match_index += len(self.competitors) // 2
        return self.get_current_round_matches()

    def is_tournament_over(self):
        return self.current_match_index >= len(self.matches)