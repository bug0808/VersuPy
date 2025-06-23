from typing import List, Optional, Union
from src.single_elim import SingleElimination
from src.match import Match
from src.competitor import Competitor

class DoubleElimination:
    def __init__(self, competitors: Union[List[str], List[Competitor]]) -> None:
        self.winners_bracket: SingleElimination = SingleElimination(competitors)
        self.losers_bracket: SingleElimination = SingleElimination([])
        self.final_match: Optional[Match] = None
        self.bracket_stage: str = "winners"

    def advance_to_next_round(self) -> None:
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
        elif self.bracket_stage == "finals" and self.final_match and self.final_match.get_winner():
            self._handle_grand_finals_reset()

    def _populate_losers_bracket(self) -> None:
        losers: List[Competitor] = []
        for match in self.winners_bracket.rounds[0]:
            loser = match.get_loser()
            if loser is not None:
                losers.append(loser)
        for competitor in losers:
            competitor.wins -= 1
        self.losers_bracket = SingleElimination(losers)

    def _setup_grand_finals(self) -> None:
        winner: Optional[Competitor] = self.winners_bracket.get_champion()
        loser_bracket_winner: Optional[Competitor] = self.losers_bracket.get_champion()
        if winner and loser_bracket_winner:
            self.final_match = Match(winner, loser_bracket_winner)

    def _handle_grand_finals_reset(self) -> None:
        if self.final_match and self.final_match.get_winner() == self.final_match.competitor_b:
            self.final_match = Match(self.final_match.competitor_a, self.final_match.competitor_b)
        else:
            self.bracket_stage = "complete"

    def is_tournament_over(self) -> bool:
        return self.bracket_stage == "complete"
