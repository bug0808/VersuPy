"""
Example: Basic Tournament Usage
This example shows how to create and run a simple single elimination tournament.
"""

from versupy.tournament import Tournament

def main():
    # Create competitors
    competitors = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"]
    
    # Create single elimination tournament
    tournament = Tournament(competitors, style="single")
    
    print("=== Single Elimination Tournament ===")
    print(f"Competitors: {[c.name for c in tournament.tournament.competitors]}")
    print()
    
    round_num = 1
    while not tournament.is_tournament_over():
        print(f"--- Round {round_num} ---")
        matches = tournament.get_current_round_matches()
        
        for i, match in enumerate(matches):
            print(f"Match {i+1}: {match.competitor_a.name} vs {match.competitor_b.name}")
            # Simulate: first competitor always wins
            winner = match.competitor_a
            tournament.set_winner(match, winner)
            print(f"  Winner: {winner.name}")
        
        print()
        tournament.advance_to_next_round()
        round_num += 1
    
    # Show final results
    champion = tournament.get_champion()
    if champion:
        print(f"🏆 Tournament Champion: {champion.name}")
    
    print("\n📊 All Results:")
    for i, (comp_a, comp_b, winner) in enumerate(tournament.get_results()):
        winner_name = winner.name if winner else 'TBD'
        print(f"  {i+1}. {comp_a.name} vs {comp_b.name} → {winner_name}")

if __name__ == "__main__":
    main()
