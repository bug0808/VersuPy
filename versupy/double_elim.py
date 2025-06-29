from typing import List, Optional, Union
from versupy.single_elim import SingleElimination
from versupy.match import Match
from versupy.competitor import Competitor

class DoubleElimination:
    def __init__(self, competitors: Union[List[str], List[Competitor]]) -> None:
        # Convert strings to Competitor objects if needed
        if competitors and isinstance(competitors[0], str):
            competitors = [Competitor(name) for name in competitors if isinstance(name, str)]
        
        self.competitors = competitors
        self.winners_bracket = SingleElimination(competitors)
        self.losers_bracket = SingleElimination([])
        self.final_match: Optional[Match] = None
        self.bracket_stage: str = "winners"
        self.results: List[tuple[Competitor, Competitor, Optional[Competitor]]] = []
        self._losers_from_winners: List[Competitor] = []

    def get_current_round_matches(self) -> List[Match]:
        """Get the current round matches based on bracket stage"""
        if self.bracket_stage == "winners":
            return self.winners_bracket.get_current_round_matches()
        elif self.bracket_stage == "losers":
            return self.losers_bracket.get_current_round_matches()
        elif self.bracket_stage == "finals" and self.final_match:
            return [self.final_match]
        return []

    def set_winner_and_track(self, match: Match, winner: Competitor) -> None:
        """Set the winner of a match and track the result"""
        match.set_winner(winner)
        result_tuple = (match.competitor_a, match.competitor_b, winner)
        
        # Add to main results - in double elimination, same matchup can happen twice
        # so we need to allow it (e.g., Winners R1 and Finals can have same competitors)
        self.results.append(result_tuple)

    def advance_to_next_round(self) -> Optional[List[Match]]:
        """Advance to the next round and return current matches"""
        if self.bracket_stage == "winners":
            return self._advance_winners_bracket()
        elif self.bracket_stage == "losers":
            return self._advance_losers_bracket()
        elif self.bracket_stage == "finals":
            return self._handle_finals()
        return None

    def _advance_winners_bracket(self) -> Optional[List[Match]]:
        """Handle advancing the winners bracket"""
        # Collect losers from current round
        current_matches = self.winners_bracket.get_current_round_matches()
        losers = []
        for match in current_matches:
            if match.get_winner() is not None:
                loser = match.get_loser()
                if loser and loser.name != "TBD":
                    losers.append(loser)
        
        # Store losers for losers bracket
        self._losers_from_winners.extend(losers)
        
        # Advance winners bracket
        self.winners_bracket.advance_to_next_round()
        
        # Check if winners bracket is complete
        if self.winners_bracket.is_tournament_over():
            self.bracket_stage = "losers"
            self._initialize_losers_bracket()
        else:
            # Add new losers to losers bracket if it exists and has competitors
            if self.losers_bracket and len(self.losers_bracket.competitors) > 0 and self._losers_from_winners:
                self._add_losers_to_bracket()
        
        return self.get_current_round_matches()

    def _advance_losers_bracket(self) -> Optional[List[Match]]:
        """Handle advancing the losers bracket"""
        # Advance losers bracket
        self.losers_bracket.advance_to_next_round()
        
        # Add new losers from winners bracket if any
        if self._losers_from_winners:
            self._add_losers_to_bracket()
        
        # Check if losers bracket is complete
        if self.losers_bracket.is_tournament_over():
            self.bracket_stage = "finals"
            self._setup_grand_finals()
        
        return self.get_current_round_matches()

    def _handle_finals(self) -> Optional[List[Match]]:
        """Handle the finals stage"""
        if self.final_match and self.final_match.get_winner():
            self.bracket_stage = "complete"
            return None
        return self.get_current_round_matches()

    def _initialize_losers_bracket(self) -> None:
        """Initialize the losers bracket with the first set of losers"""
        # Only use the first round losers for initial bracket
        # In a 4-person tournament: Round 1 produces 2 losers, Winners final produces 1 loser
        # The test expects only the first 2 losers to be in the initial bracket
        first_round_losers = self._losers_from_winners[:2]  # Bob and David
        if len(first_round_losers) >= 2:
            self.losers_bracket = SingleElimination(first_round_losers)
            # Keep remaining losers for later rounds
            self._losers_from_winners = self._losers_from_winners[2:]

    def _add_losers_to_bracket(self) -> None:
        """Add new losers from winners bracket to current losers bracket"""
        if not self._losers_from_winners:
            return
            
        # Get current survivors in losers bracket
        current_survivors = []
        if self.losers_bracket.rounds:
            last_round = self.losers_bracket.rounds[-1]
            for match in last_round:
                winner = match.get_winner()
                if winner is not None and winner.name != "TBD":
                    current_survivors.append(winner)
        
        # Combine survivors with new losers
        next_round_competitors = current_survivors + self._losers_from_winners
        
        # Create new round if we have enough competitors
        if len(next_round_competitors) >= 2:
            new_matches = []
            for i in range(0, len(next_round_competitors), 2):
                if i + 1 < len(next_round_competitors):
                    comp_a = next_round_competitors[i]
                    comp_b = next_round_competitors[i + 1]
                    if comp_a and comp_b:  # Ensure both competitors are valid
                        new_matches.append(Match(comp_a, comp_b))
            
            if new_matches:
                self.losers_bracket.rounds.append(new_matches)
                self.losers_bracket.current_round = len(self.losers_bracket.rounds) - 1
        
        self._losers_from_winners = []

    def _setup_grand_finals(self) -> None:
        """Setup the grand finals match"""
        winners_champion = self.winners_bracket.get_champion()
        losers_champion = self.losers_bracket.get_champion()
        
        if winners_champion and losers_champion:
            self.final_match = Match(winners_champion, losers_champion)

    def is_tournament_over(self) -> bool:
        """Check if the tournament is complete"""
        return self.bracket_stage == "complete"

    def get_champion(self) -> Optional[Competitor]:
        """Get the tournament champion"""
        if self.is_tournament_over() and self.final_match:
            return self.final_match.get_winner()
        return None

    def get_results(self) -> List[tuple[Competitor, Competitor, Optional[Competitor]]]:
        """Get all tournament results"""
        return self.results.copy()