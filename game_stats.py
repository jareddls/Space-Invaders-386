import pickle

class GameStats():
    """Track statistics for Space Invaders."""
    
    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.reset_stats()
        
        # Start game in an inactive state.
        self.game_active = False
        
        # High score should never be reset.
        # self.high_score = 0
        try:
            with open('scores/high_scores.dat', 'rb') as file:
                self.high_score = pickle.load(file)
        except:
            self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1