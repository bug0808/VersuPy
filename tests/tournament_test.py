import pytest
from versupy.competitor import Competitor
from versupy.tournament import Tournament
from versupy.match import Match

@pytest.mark.parametrize("style", ["single", "double", "round_robin", "swiss"])
def test_generate_bracket(style):
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors, style)
    assert hasattr(bracket.tournament, "rounds")
    assert len(bracket.tournament.rounds) == 1 or style in ["round_robin", "swiss"]

@pytest.mark.parametrize("style", ["single", "double", "round_robin", "swiss"])
def test_advance_to_next_round(style):
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors, style)
    matches = bracket.get_current_round_matches()
    # Set winners for the first round
    for match in matches:
        match.set_winner(match.competitor_a)
    next_round = bracket.advance_to_next_round()
    # For round robin/swiss, next_round may be None if only one round
    if style in ["single", "double"]:
        assert next_round is not None
        assert all(isinstance(m, Match) for m in next_round)

@pytest.mark.parametrize("style", ["single", "double", "round_robin", "swiss"])
def test_bracket_with_odd_number_of_competitors(style):
    competitors = ["Alice", "Bob", "Charlie"]
    bracket = Tournament(competitors, style)
    # For elimination, there should be a 'TBD' or bye
    if style in ["single", "double"]:
        assert any("TBD" in (m.competitor_a.name, m.competitor_b.name) for m in bracket.tournament.rounds[0])
    else:
        # For round robin/swiss, all competitors should be present
        assert all(any(c.name == name for c in bracket.tournament.competitors) for name in competitors)

@pytest.mark.parametrize("style", ["single", "double", "round_robin", "swiss"])
def test_get_current_round_matches(style):
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors, style)
    matches = bracket.get_current_round_matches()
    assert all(isinstance(m, Match) for m in matches)
    # For elimination, check first match names
    if style in ["single", "double"]:
        assert matches[0].competitor_a.name == "Alice"
        assert matches[0].competitor_b.name == "Bob"