from src.round_robin import RoundRobin
from src.competitor import Competitor

def test_round_robin_initialization():
    competitors = [Competitor("Alice"), Competitor("Bob"), Competitor("Charlie"), Competitor("David")]
    rr = RoundRobin(competitors)
    # For 4 competitors, there should be 6 matches (n*(n-1)/2)
    assert len(rr.matches) == 6
    assert rr.current_match_index == 0

def test_get_current_round_matches():
    competitors = [Competitor("Alice"), Competitor("Bob"), Competitor("Charlie"), Competitor("David")]
    rr = RoundRobin(competitors)
    round_matches = rr.get_current_round_matches()
    # Each round should have 2 matches for 4 competitors
    assert len(round_matches) == 2

def test_advance_to_next_round():
    competitors = [Competitor("Alice"), Competitor("Bob"), Competitor("Charlie"), Competitor("David")]
    rr = RoundRobin(competitors)
    rr.get_current_round_matches()  # round 1
    rr.advance_to_next_round()      # round 2
    assert rr.current_match_index == 2
    round_matches = rr.get_current_round_matches()
    assert len(round_matches) == 2

def test_is_tournament_over():
    competitors = [Competitor("Alice"), Competitor("Bob"), Competitor("Charlie"), Competitor("David")]
    rr = RoundRobin(competitors)
    # Advance through all rounds
    while not rr.is_tournament_over():
        rr.advance_to_next_round()
    assert rr.is_tournament_over()

def test_results_tracking_round_robin():
    competitors = [Competitor("Alice"), Competitor("Bob"), Competitor("Charlie"), Competitor("David")]
    rr = RoundRobin(competitors)
    # Play all rounds
    while not rr.is_tournament_over():
        for match in rr.get_current_round_matches():
            match.set_winner(match.competitor_a)
        rr.advance_to_next_round()
    # There should be 6 results (for 4 competitors: 4*3/2 = 6 matches)
    assert len(rr.results) == 6
    for result in rr.results:
        assert result[2] is not None