from versupy.competitor import Competitor

def test_create_competitor():
    """Test creating a competitor."""
    player = Competitor("Alice")
    assert player.name == "Alice"
    assert player.wins == 0

def test_create_competitor_with_wins():
    """Test creating a competitor with wins."""
    player = Competitor("Bob", 2)
    assert player.name == "Bob"
    assert player.wins == 2

def test_update_wins():
    """Test updating the wins of a competitor."""
    player = Competitor("Charlie", 1)
    player.wins += 1
    assert player.wins == 2

def test_change_name():
    """Test changing the name of a competitor."""
    player = Competitor("Dave")
    player.name = "David"
    assert player.name == "David"

def test_default_wins():
    """Test the default wins value."""
    player = Competitor("Eve")
    assert player.wins == 0
