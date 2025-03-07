from .single_elim import SingleElimination
from .match import Match

class DoubleElimination:
    def __init__(self, competitors):
        """Initialize double elimination with winners & losers brackets."""
        self.winners_bracket = SingleElimination(competitors)
        self.losers_bracket = SingleElimination([])
        self.final_match = None
        self.bracket_stage = "winners"

    def advance_to_next_round(self):
        """Advance through winners, then losers, then grand finals if needed."""
        if self.bracket_stage == "winners":
            self.winners_bracket.advance_to_next_round()
            
            if self.winners_bracket.is_tournament_over():
                self.bracket_stage = "losers"
                self._populate_losers_bracket()

        elif self.bracket_stage == "losers":
            self.losers_bracket.advance_to_next_round()

            if self.losers_bracket.is_tournament_over():
                self.bracket_stage = "finals"
                self._setup_grand_finals()

        elif self.bracket_stage == "finals" and self.final_match.get_winner():
            self._handle_grand_finals_reset()

    def _populate_losers_bracket(self):
        """Move first-round losers to the losers' bracket."""
        losers = [match.get_loser() for match in self.winners_bracket.rounds[0] if match.get_loser()]
        for competitor in losers:
            competitor.wins -= 1  # Deduct a win since this is double elimination

        self.losers_bracket = SingleElimination(losers)

    def _setup_grand_finals(self):
        """Create the grand finals match."""
        winner = self.winners_bracket.get_champion()
        loser_bracket_winner = self.losers_bracket.get_champion()
        self.final_match = Match(winner, loser_bracket_winner)

    def _handle_grand_finals_reset(self):
        """Check if the losers' bracket winner forces a bracket reset."""
        if self.final_match.get_winner() == self.final_match.competitor_b:
            # Reset and play one final match
            self.final_match = Match(self.final_match.competitor_a, self.final_match.competitor_b)
        else:
            self.bracket_stage = "complete"

    def is_tournament_over(self):
        return self.bracket_stage == "complete"
