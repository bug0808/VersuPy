from .single_elim import SingleElimination
from .double_elim import DoubleElimination
from .round_robin import RoundRobin
from .swiss import Swiss

class Tournament:
    """A tournament bracket for a given set of competitors."""
    def __init__(self, competitors, style="single"):
        """Initialize a tournament bracket of the selected style."""
        self.style = style.lower()

        if self.style == "single":
            self.tournament = SingleElimination(competitors)
        elif self.style == "double":
            self.tournament = DoubleElimination(competitors)
        elif self.style == "round_robin":
            self.tournament = RoundRobin(competitors)
        elif self.style == "swiss":
            self.tournament = Swiss(competitors)
        else:
            raise ValueError("Invalid tournament style. Choose from: single, double, round_robin, swiss.")

    def get_current_round_matches(self):
        """Get matches for the current round."""
        return self.tournament.get_current_round_matches()

    def advance_to_next_round(self):
        """Advance the tournament to the next round."""
        return self.tournament.advance_to_next_round()

    def is_tournament_over(self):
        """Check if the tournament has concluded."""
        return self.tournament.is_tournament_over()