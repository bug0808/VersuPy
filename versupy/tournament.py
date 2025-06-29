from typing import List, Union, Optional, Any
from versupy.single_elim import SingleElimination
from versupy.double_elim import DoubleElimination
from versupy.round_robin import RoundRobin
from versupy.swiss import Swiss
from versupy.competitor import Competitor
from versupy.match import Match

class Tournament:
    """
    A tournament bracket for a given set of competitors.
    Supports single elimination, double elimination, round robin, and swiss formats.
    """
    def __init__(self, competitors: Union[List[str], List[Competitor]], style: str) -> None:
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

    def set_winner(self, match: Match, winner: Competitor) -> None:
        """
        Set the winner of a match.

        Args:
            match: The match to set the winner for.
            winner: The competitor who won the match.
        """
        if hasattr(self.tournament, "set_winner_and_track"):
            self.tournament.set_winner_and_track(match, winner)
        else:
            match.set_winner(winner)

    def get_results(self) -> List[tuple[Competitor, Competitor, Optional[Competitor]]]:
        """
        Get all tournament results.

        Returns:
            List of result tuples (competitor_a, competitor_b, winner).
        """
        if hasattr(self.tournament, "get_results"):
            return self.tournament.get_results()
        return []