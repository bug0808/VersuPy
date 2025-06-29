from versupy.competitor import Competitor
from versupy.swiss import Swiss


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

    # Simulate round 1
    round_1_matches = swiss.generate_round()
    for match in round_1_matches:
        match.set_winner(match.competitor_a)
    # Simulate round 2
    swiss.advance_round()
    round_2_matches = swiss.generate_round()
    for match in round_2_matches:
        match.set_winner(match.competitor_a)

    # Now calculate Buchholz scores
    buchholz_scores = swiss.calculate_buchholz_scores()
    # The player with the most wins should have a higher Buchholz score
    standings = sorted(swiss.competitors, key=lambda c: c.wins, reverse=True)
    assert buchholz_scores[standings[0].name] >= buchholz_scores[standings[1].name]

def test_results_tracking_swiss():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    swiss = Swiss(competitors)
    # Round 1
    round_1_matches = swiss.generate_round()
    for match in round_1_matches:
        match.set_winner(match.competitor_a)
    swiss.record_match_results([match.competitor_a for match in round_1_matches])
    # Round 2
    swiss.advance_round()
    round_2_matches = swiss.generate_round()
    for match in round_2_matches:
        match.set_winner(match.competitor_b)
    swiss.record_match_results([match.competitor_b for match in round_2_matches])
    # There should be 4 results (2 per round)
    assert len(swiss.results) == 4
    for result in swiss.results:
        assert result[2] is not None