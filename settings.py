import random
import pygame as pg

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 700
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        
# # TODO: test laser with a really wide laser
        # self.laser_width = 500
        # self.laser_height = 30
        # self.laser_color = 255, 0, 0
        self.lasers_every = 150

        self.alien0_points = 50
        self.alien1_points = 100
        self.alien2_points = 150

        mystery_points = {'alien0': 50, 'alien1': 100, 'alien2': 150, 'ufo_max': 200}
        self.ufo_points = random.choice(list(mystery_points.keys()))
# # TODO: set a ship_limit of 3
        self.ship_limit = 3         # total ships allowed in game before game over

        self.fleet_drop_speed = 20
        self.fleet_direction = 1     # change to a Vector(1, 0) move to the right, and ...
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.alien_speed_factor = 0.09
        self.ship_speed_factor = 0.5
        self.laser_speed_factor = 1

    # def increase_speed(self):
    #     pass
    #     # scale = self.speedup_scale
    #     # self.ship_speed_factor *= scale
    #     # # self.laser_speed_factor *= scale
