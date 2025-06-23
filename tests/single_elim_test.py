import pytest
from src.single_elim import SingleElimination
from src.competitor import Competitor

def test_single_elim_initialization():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    se = SingleElimination(competitors)
    # Should create 2 matches for 4 competitors
    assert len(se.rounds) == 1
    assert len(se.rounds[0]) == 2

def test_advance_to_next_round():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    se = SingleElimination(competitors)
    # Set winners for round 1
    for match in se.get_current_round_matches():
        match.set_winner(match.competitor_a)
    next_round = se.advance_to_next_round()
    assert next_round is not None
    assert len(next_round) == 1  # Final match

def test_tournament_over():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    se = SingleElimination(competitors)
    # Round 1
    for match in se.get_current_round_matches():
        match.set_winner(match.competitor_a)
    se.advance_to_next_round()
    # Final round
    final_match = se.get_current_round_matches()[0]
    final_match.set_winner(final_match.competitor_a)
    assert se.is_tournament_over()

def test_bye_round():
    competitors = ["Alice", "Bob", "Charlie"]  # Odd number, should add a "TBD"
    se = SingleElimination(competitors)
    # Should pad to 4 competitors, so 2 matches
    assert len(se.rounds[0]) == 2

def test_results_tracking_single_elim():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    se = SingleElimination(competitors)
    # Round 1
    for match in se.get_current_round_matches():
        match.set_winner(match.competitor_a)
    se.advance_to_next_round()
    # Final round
    final_match = se.get_current_round_matches()[0]
    final_match.set_winner(final_match.competitor_a)
    se.advance_to_next_round()
    # There should be 3 results (2 in round 1, 1 in final)
    assert len(se.results) == 3
    # Each result is a tuple (competitor_a, competitor_b, winner)
    for result in se.results:
        assert result[2] is not None