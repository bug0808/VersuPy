# VersuPy

A comprehensive Python library for creating and managing tournament brackets with automated match handling.

## Features

- 🏆 **Multiple Tournament Formats**: Single elimination, double elimination, round robin, and Swiss system
- 🎯 **Clean API**: Easy-to-use interface for tournament management
- 📊 **Result Tracking**: Comprehensive match and tournament result tracking
- 🧪 **Well Tested**: Extensive test coverage for all tournament formats
- 🔧 **Type Safe**: Full type hint support for better development experience

## Installation

```bash
pip install versupy
```

## Quick Start

```python
from versupy import Tournament

# Create a single elimination tournament
competitors = ["Alice", "Bob", "Charlie", "David"]
tournament = Tournament(competitors, style="single")

# Get current round matches
matches = tournament.get_current_round_matches()

# Set match winners
for match in matches:
    tournament.set_winner(match, match.competitor_a)  # Alice and Charlie win

# Advance to next round
tournament.advance_to_next_round()

# Check if tournament is complete
if tournament.is_tournament_over():
    champion = tournament.get_champion()
    print(f"Tournament winner: {champion.name}")
```

## Tournament Formats

### Single Elimination
```python
tournament = Tournament(competitors, style="single")
```

### Double Elimination
```python
tournament = Tournament(competitors, style="double")
```

### Round Robin
```python
tournament = Tournament(competitors, style="round_robin")
```

### Swiss System
```python
tournament = Tournament(competitors, style="swiss")
```

## API Reference

### Tournament Class

- `get_current_round_matches()` - Get matches for the current round
- `set_winner(match, winner)` - Set the winner of a match
- `advance_to_next_round()` - Progress to the next round
- `is_tournament_over()` - Check if tournament is complete
- `get_champion()` - Get the tournament winner
- `get_results()` - Get all match results

### Match Class

- `set_winner(competitor)` - Set match winner
- `get_winner()` - Get match winner
- `get_loser()` - Get match loser

### Competitor Class

- `name` - Competitor name
- `wins` - Number of wins
- `matches` - List of matches played

## Examples

See the `examples/` directory for more detailed usage examples.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
