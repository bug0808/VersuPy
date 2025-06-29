from versupy.double_elim import DoubleElimination

def test_double_elim_initialization():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    de = DoubleElimination(competitors)
    assert len(de.winners_bracket.competitors) == 4
    assert de.losers_bracket is None or len(de.losers_bracket.competitors) == 0
    assert de.bracket_stage == "winners"

def test_winners_to_losers_transition():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    de = DoubleElimination(competitors)
    # Simulate winners for round 1
    for match in de.winners_bracket.get_current_round_matches():
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    # Simulate winner for final match in winners bracket
    for match in de.winners_bracket.get_current_round_matches():
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()  # This should now move to losers bracket
    assert de.bracket_stage == "losers"
    # Losers bracket may not be populated until after this call
    assert len(de.losers_bracket.competitors) == 2

def test_losers_to_finals_transition():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    de = DoubleElimination(competitors)
    # Simulate winners bracket
    for match in de.winners_bracket.get_current_round_matches():
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    for match in de.winners_bracket.get_current_round_matches():
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    # Simulate losers bracket
    losers_matches = de.losers_bracket.get_current_round_matches()
    for match in losers_matches:
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    losers_matches = de.losers_bracket.get_current_round_matches()
    for match in losers_matches:
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    assert de.bracket_stage == "finals"
    assert de.final_match is not None

def test_tournament_completion():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    de = DoubleElimination(competitors)
    # Simulate winners bracket
    for match in de.winners_bracket.get_current_round_matches():
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    for match in de.winners_bracket.get_current_round_matches():
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    # Simulate losers bracket
    losers_matches = de.losers_bracket.get_current_round_matches()
    for match in losers_matches:
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    losers_matches = de.losers_bracket.get_current_round_matches()
    for match in losers_matches:
        match.set_winner(match.competitor_a)
    de.advance_to_next_round()
    # Simulate finals
    assert de.final_match is not None
    de.final_match.set_winner(de.final_match.competitor_a)
    de.advance_to_next_round()
    assert de.is_tournament_over()

def test_results_tracking_double_elim():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    de = DoubleElimination(competitors)
    # Winners bracket round 1
    for match in de.winners_bracket.get_current_round_matches():
        de.set_winner_and_track(match, match.competitor_a)
    de.advance_to_next_round()
    # Winners bracket round 2
    for match in de.winners_bracket.get_current_round_matches():
        de.set_winner_and_track(match, match.competitor_a)
    de.advance_to_next_round()
    # Losers bracket round 1
    for match in de.losers_bracket.get_current_round_matches():
        de.set_winner_and_track(match, match.competitor_a)
    de.advance_to_next_round()
    # Losers bracket round 2 (THIS WAS MISSING!)
    for match in de.losers_bracket.get_current_round_matches():
        de.set_winner_and_track(match, match.competitor_a)
    de.advance_to_next_round()
    # Finals
    assert de.final_match is not None
    de.set_winner_and_track(de.final_match, de.final_match.competitor_a)
    de.advance_to_next_round()
    # There should be 6 results (2 winners R1, 1 winners final, 2 losers, 1 final)
    assert len(de.results) == 6
    for result in de.results:
        assert result[2] is not None