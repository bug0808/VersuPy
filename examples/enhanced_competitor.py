"""
Enhanced Competitor class with more features
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from versupy.match import Match

class EnhancedCompetitor:
    """Enhanced competitor with additional features for professional tournaments."""
    
    def __init__(
        self, 
        name: str, 
        seed: Optional[int] = None,
        rating: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        self.name = name
        self.seed = seed  # Tournament seeding
        self.rating = rating  # ELO or skill rating
        self.metadata = metadata or {}  # Additional data (team, country, etc.)
        
        # Tournament stats
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.points = 0.0
        self.buchholz_score = 0.0
        self.has_bye = False
        
        # Match history
        self.matches: List["Match"] = []
        self.opponents_played: List["EnhancedCompetitor"] = []
        
        # Timestamps
        self.created_at = datetime.now()
        self.last_match_at: Optional[datetime] = None
    
    @property
    def win_rate(self) -> float:
        """Calculate win percentage."""
        total_games = self.wins + self.losses + self.draws
        return self.wins / total_games if total_games > 0 else 0.0
    
    @property
    def total_matches(self) -> int:
        """Total matches played."""
        return self.wins + self.losses + self.draws
    
    def add_win(self, opponent: "EnhancedCompetitor") -> None:
        """Record a win against an opponent."""
        self.wins += 1
        self.last_match_at = datetime.now()
        if opponent not in self.opponents_played:
            self.opponents_played.append(opponent)
    
    def add_loss(self, opponent: "EnhancedCompetitor") -> None:
        """Record a loss against an opponent."""
        self.losses += 1
        self.last_match_at = datetime.now()
        if opponent not in self.opponents_played:
            self.opponents_played.append(opponent)
    
    def add_draw(self, opponent: "EnhancedCompetitor") -> None:
        """Record a draw against an opponent."""
        self.draws += 1
        self.last_match_at = datetime.now()
        if opponent not in self.opponents_played:
            self.opponents_played.append(opponent)
    
    def has_played(self, opponent: "EnhancedCompetitor") -> bool:
        """Check if this competitor has played against another."""
        return opponent in self.opponents_played
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "seed": self.seed,
            "rating": self.rating,
            "metadata": self.metadata,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "points": self.points,
            "buchholz_score": self.buchholz_score,
            "win_rate": self.win_rate,
            "total_matches": self.total_matches,
            "created_at": self.created_at.isoformat(),
            "last_match_at": self.last_match_at.isoformat() if self.last_match_at else None
        }
    
    def __repr__(self) -> str:
        return f"EnhancedCompetitor(name='{self.name}', wins={self.wins}, rating={self.rating})"
