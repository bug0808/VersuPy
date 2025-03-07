from .match import Match
from .competitor import Competitor

class Swiss:
    def __init__(self, competitors, rounds=None):
        """Initialize a Swiss-system tournament."""
        self.competitors = [Competitor(name) for name in competitors]  # Ensure competitors are Competitor objects
        self.round = 1  # Initialize the round attribute
        self.rounds_played = 0
        self.max_rounds = rounds if rounds else len(competitors) - 1  # Default: log2(n)
        self.matches = []

    def generate_round(self):
        """Generate pairings for the next round."""
        self.generate_round_pairings()  # Reuse existing method
        self.round += 1  # Increment the round number

    def generate_round_pairings(self):
        """Pair competitors with similar win records for the next round."""
        self.competitors.sort(key=lambda c: c.wins, reverse=True)  # Sort by wins
        new_matches = []
        bye_player = None

        # Handle odd number of players: Assign a bye
        if len(self.competitors) % 2 == 1:
            for competitor in reversed(self.competitors):  # Give bye to lowest-ranked available player
                if not hasattr(competitor, "has_bye"):  # Ensure each player gets only one bye
                    competitor.wins += 1  # Free win
                    competitor.has_bye = True  # Mark as having received a bye
                    bye_player = competitor
                    self.competitors.remove(competitor)
                    break

        # Pair remaining competitors
        while len(self.competitors) > 1:
            a, b = self.competitors.pop(0), self.competitors.pop(0)
            match = Match(a, b)
            new_matches.append(match)
            a.matches.append(match)  # Track match for competitor 'a'
            b.matches.append(match)  # Track match for competitor 'b'

        self.matches.append(new_matches)
        return new_matches  # Return the generated matches for this round

    def record_match_results(self, results):
        """Update wins based on match results."""
        for match, winner in zip(self.matches[-1], results):
            match.set_winner(winner)
            winner.wins += 1  # Increase wins for the winner

    def calculate_buchholz_scores(self):
        """Calculate the Buchholz score for each competitor and return it as a dictionary."""
        buchholz_scores = {}
        for competitor in self.competitors:
            competitor.buchholz_score = 0  # Initialize score
            for match in competitor.matches:
                opponent = match.competitor_a if match.competitor_b == competitor else match.competitor_b
                competitor.buchholz_score += opponent.wins  # Sum opponent wins
            buchholz_scores[competitor.name] = competitor.buchholz_score  # Add to dictionary

        return buchholz_scores  # Return the dictionary with Buchholz scores
    
    def advance_to_next_round(self):
        """Proceed to the next round if there are remaining rounds."""
        if self.rounds_played < self.max_rounds:
            self.generate_round_pairings()
            self.rounds_played += 1

    def get_standings(self):
        """Return competitors sorted by their final standings, considering Buchholz if necessary."""
        # Sort by wins first, then by Buchholz score if tied
        self.competitors.sort(key=lambda c: (c.wins, c.buchholz_score), reverse=True)
        return self.competitors

    def is_tournament_over(self):
        return self.rounds_played >= self.max_rounds