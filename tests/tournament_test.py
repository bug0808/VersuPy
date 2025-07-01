import pytest
from versupy.competitor import Competitor
from versupy.tournament import Tournament
from versupy.match import Match

@pytest.mark.parametrize("style", ["single", "double", "round_robin", "swiss"])
def test_generate_bracket(style):
    competitors = ["Alice", "Bob", "Charlie", "David"]
    bracket = Tournament(competitors, style)
    t = bracket.tournament
    if style == "single":
        assert hasattr(t, "rounds")
        assert len(t.rounds) == 1
    elif style == "double":
        # DoubleElimination has winners_bracket and losers_bracket
        assert hasattr(t, "winners_bracket")
        assert hasattr(t.winners_bracket, "rounds")
        assert len(t.winners_bracket.rounds) == 1
    elif style == "round_robin":
        # RoundRobin has matches instead of rounds
        assert hasattr(t, "matches")
        # For 4 competitors, there should be 6 matches (n*(n-1)/2)
        assert len(t.matches) == 6
    elif style == "swiss":
        assert hasattr(t, "rounds")

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
    t = bracket.tournament
    if style == "single":
        assert any("TBD" in (m.competitor_a.name, m.competitor_b.name) for m in t.rounds[0])
    elif style == "double":
        assert any("TBD" in (m.competitor_a.name, m.competitor_b.name) for m in t.winners_bracket.rounds[0])
    else:
        assert all(any(c.name == name for c in t.competitors) for name in competitors)

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