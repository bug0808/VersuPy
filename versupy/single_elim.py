from typing import List, Optional
from versupy.match import Match
from versupy.competitor import Competitor
import math

class SingleElimination:
    """Single elimination tournament system."""

    def __init__(self, competitors: list[str] | list[Competitor]) -> None:
        """
        Initialize the single elimination bracket.

        Args:
            competitors: List of competitor names or Competitor objects.
        """
        self.competitors: List[Competitor] = [c if isinstance(c, Competitor) else Competitor(c) for c in competitors]
        self.rounds: List[List[Match]] = []
        self.current_round: int = 0
        self.results: List[tuple[Competitor, Competitor, Optional[Competitor]]] = []
        self.generate_bracket()

    def generate_bracket(self) -> None:
        """Create the initial bracket, padding with 'TBD' if needed."""
        if len(self.competitors) < 2:
            return
        next_power_of_2 = 2 ** math.ceil(math.log2(len(self.competitors)))
        while len(self.competitors) < next_power_of_2:
            self.competitors.append(Competitor("TBD"))
        self.rounds.append([Match(self.competitors[i], self.competitors[i + 1])
                            for i in range(0, len(self.competitors), 2)])

    def get_current_round_matches(self) -> List[Match]:
        """Return the matches for the current round."""
        return self.rounds[self.current_round]

    def advance_to_next_round(self) -> Optional[List[Match]]:
        """
        Advance to the next round by pairing winners.

        Returns:
            The list of matches for the next round, or None if tournament is over.
        """
        current_matches = self.get_current_round_matches()
        # Track results for the current round
        for match in current_matches:
            if match.get_winner() is not None:
                self.results.append((match.competitor_a, match.competitor_b, match.get_winner()))
        winners = [winner for match in current_matches if (winner := match.get_winner()) is not None]
        if len(winners) < 2:
            # If this is the final match, ensure its result is tracked
            if len(current_matches) == 1 and current_matches[0].get_winner() is not None:
                # Already tracked above, so nothing more to do
                pass
            return None
        next_round_matches: List[Match] = []
        i = 0
        while i < len(winners):
            if i + 1 < len(winners):
                next_round_matches.append(Match(winners[i], winners[i + 1]))
                i += 2
            else:
                # Odd competitor advances automatically (bye)
                next_round_matches.append(Match(winners[i], Competitor("TBD")))
                i += 1
        self.rounds.append(next_round_matches)
        self.current_round += 1
        return next_round_matches

    def is_tournament_over(self) -> bool:
        """Return True if the tournament has a champion."""
        return len(self.rounds[-1]) == 1 and self.rounds[-1][0].get_winner() is not None

    def get_champion(self) -> Optional[Competitor]:
        """Return the champion if the tournament is over, else None."""
        if self.is_tournament_over():
            return self.rounds[-1][0].get_winner()
        return None