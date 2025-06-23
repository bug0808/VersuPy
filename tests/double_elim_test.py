from src.double_elim import DoubleElimination

def test_double_elim_initialization():
    competitors = ["Alice", "Bob", "Charlie", "David"]
    de = DoubleElimination(competitors)
    assert len(de.winners_bracket.competitors) == 4
    assert len(de.losers_bracket.competitors) == 0
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