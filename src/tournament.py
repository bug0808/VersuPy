from typing import List, Union, Optional, Any
from src.single_elim import SingleElimination
from src.double_elim import DoubleElimination
from src.round_robin import RoundRobin
from src.swiss import Swiss
from src.competitor import Competitor
from src.match import Match

class Tournament:
    """
    A tournament bracket for a given set of competitors.
    Supports single elimination, double elimination, round robin, and swiss formats.
    """
    def __init__(self, competitors: Union[List[str], List[Competitor]], style: str = "single") -> None:
        """
        Initialize a tournament bracket of the selected style.

        Args:
            competitors: List of competitor names or Competitor objects.
            style: The tournament style ("single", "double", "round_robin", "swiss").
        """
        self.style: str = style.lower()
        self.tournament: Any

        # Always convert to List[Competitor]
        competitors_list: List[Competitor] = [c if isinstance(c, Competitor) else Competitor(c) for c in competitors]

        if self.style == "single":
            self.tournament = SingleElimination(competitors_list)
        elif self.style == "double":
            self.tournament = DoubleElimination(competitors_list)
        elif self.style == "round_robin":
            self.tournament = RoundRobin(competitors_list)
        elif self.style == "swiss":
            self.tournament = Swiss(competitors_list)
        else:
            raise ValueError("Invalid tournament style. Choose from: single, double, round_robin, swiss.")

    def get_current_round_matches(self) -> List[Match]:
        """
        Get matches for the current round.

        Returns:
            List of Match objects for the current round.
        """
        return self.tournament.get_current_round_matches()

    def advance_to_next_round(self) -> Optional[List[Match]]:
        """
        Advance the tournament to the next round.

        Returns:
            List of Match objects for the next round, or None if the tournament is over.
        """
        return self.tournament.advance_to_next_round()

    def is_tournament_over(self) -> bool:
        """
        Check if the tournament has concluded.

        Returns:
            True if the tournament is over, False otherwise.
        """
        return self.tournament.is_tournament_over()

    def get_champion(self) -> Optional[Competitor]:
        """
        Return the champion if the tournament is over.

        Returns:
            The winning Competitor, or None if the tournament is not over.
        """
        if hasattr(self.tournament, "get_champion"):
            return self.tournament.get_champion()