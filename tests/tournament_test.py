import pytest
from VersuPy.competitor import Competitor
from VersuPy.tournament import Tournament
from VersuPy.match import Match



def test_generate_bracket():
    """Test generating a tournament bracket."""
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors)

    # Access rounds from the correct tournament style (e.g., single elimination)
    assert len(bracket.tournament.rounds) == 1  # Only the first round

def test_advance_to_next_round():
    """Test advancing to the next round."""
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors)

    # Set winners for the first round
    match_1 = bracket.get_current_round_matches()[0]
    match_1.set_winner(match_1.competitor_a)  # Alice wins
    match_2 = bracket.get_current_round_matches()[1]
    match_2.set_winner(match_2.competitor_b)  # David wins

    # Advance to the next round
    next_round = bracket.advance_to_next_round()
    assert len(next_round) == 1  # Only one match in the second round
    assert next_round[0].competitor_a == match_1.get_winner()  # Alice
    assert next_round[0].competitor_b == match_2.get_winner()  # David

def test_bracket_with_odd_number_of_competitors():
    """Test bracket generation with an odd number of competitors (bye)."""
    competitors = ["Alice", "Bob", "Charlie"]
    bracket = Tournament(competitors)

    # Ensure there is a 'TBD' competitor for the bye
    assert len(bracket.tournament.rounds[0]) == 2  # 2 matches

def test_get_current_round_matches():
    """Test fetching current round matches."""
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors)
    matches = bracket.get_current_round_matches()

    assert len(matches) == 2  # First round has 2 matches
    assert matches[0].competitor_a.name == "Alice"
    assert matches[0].competitor_b.name == "Bob"
