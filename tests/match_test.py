import pytest
from VersuPy.competitor import Competitor
from VersuPy.match import Match


def test_match_initialization():
    """Test the initialization of a match."""
    competitor_a = Competitor("Alice")
    competitor_b = Competitor("Bob")
    match = Match(competitor_a, competitor_b)

    assert match.competitor_a == competitor_a
    assert match.competitor_b == competitor_b
    assert match.winner is None


def test_set_winner():
    """Test setting a winner in the match."""
    competitor_a = Competitor("Alice")
    competitor_b = Competitor("Bob")
    match = Match(competitor_a, competitor_b)

    match.set_winner(competitor_a)
    assert match.winner == competitor_a

    with pytest.raises(ValueError):
        match.set_winner(Competitor("Charlie"))  # Invalid competitor


def test_get_winner():
    """Test getting the winner of a match."""
    competitor_a = Competitor("Alice")
    competitor_b = Competitor("Bob")
    match = Match(competitor_a, competitor_b)

    match.set_winner(competitor_a)
    assert match.get_winner() == competitor_a
