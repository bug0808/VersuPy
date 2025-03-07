import pytest
from VersuPy.competitor import Competitor
from VersuPy.swiss import Swiss


def test_swiss_initialization():
    """Test Swiss tournament initialization."""
    competitors = ["Alice", "Bob", "Charlie", "David"]
    swiss = Swiss(competitors)

    assert len(swiss.competitors) == 4
    assert swiss.round == 1  # Starts from round 1


def test_swiss_rounds():
    """Test the progression of rounds in Swiss system."""
    competitors = ["Alice", "Bob", "Charlie", "David"]
    swiss = Swiss(competitors)

    round_1_matches = swiss.generate_round()
    assert len(round_1_matches) == 2  # Round 1 should have 2 matches

    # Simulate winners for round 1
    for match in round_1_matches:
        match.set_winner(match.competitor_a)  # Assume competitor_a wins each match

    # Progress to next round
    swiss.advance_round()
    round_2_matches = swiss.generate_round()
    assert len(round_2_matches) == 2  # Round 2 should also have 2 matches


def test_buchholz_score():
    """Test Buchholz scoring system (tie-breaker)."""
    competitors = ["Alice", "Bob", "Charlie"]
    swiss = Swiss(competitors)

    # Simulate wins and losses
    alice = swiss.competitors[0]
    bob = swiss.competitors[1]
    charlie = swiss.competitors[2]

    alice.wins = 2
    bob.wins = 1
    charlie.wins = 1

    # Compute Buchholz score (just an example logic)
    buchholz_scores = swiss.calculate_buchholz_scores()
    assert buchholz_scores[alice.name] > buchholz_scores[bob.name]  # Alice should have higher score
