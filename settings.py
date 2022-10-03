import random
import pygame as pg

class Settings():
    """A class to store all settings for Alien Invasion."""
    increment = 1
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 700
        self.screen_height = 800
        self.bg = pg.image.load('images/start_screen.png')
        self.bg_color = (0, 0, 0)

        self.lasers_every = 150

        self.aliens_shoot_every = 600

        self.alien0_points = 50
        self.alien1_points = 100
        self.alien2_points = 150

        mystery_points = {'alien0': 50, 'alien1': 100, 'alien2': 150, 'ufo_max': 200}
        self.ufo_points = random.choice(list(mystery_points.keys()))

        self.speedup_scale = 1.5

        self.ship_limit = 3      # total ships allowed in game before game over

        self.fleet_drop_speed = 15
        self.fleet_direction = 1     # change to a Vector(1, 0) move to the right, and ...
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.alien_speed_factor = 0.09
        self.ship_speed_factor = 1
        self.laser_speed_factor = 1

    def increase_speed(self):
        self.increment += 1
        scale = self.speedup_scale
        if self.lasers_every > 50:
            self.lasers_every -= 20 #how much lasers show up every level goes faster 
        # self.ship_speed_factor *= scale
        self.alien_speed_factor *= scale
        # self.laser_speed_factor *= scale
