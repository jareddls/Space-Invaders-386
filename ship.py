import pygame as pg
import time
from timer import Timer
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector
from sys import exit


class Ship(Sprite):
    ship_explosion_images = [pg.image.load(f'images/ship_explosion{n}.png') for n in range(12)]
    ship_reg_image = [pg.image.load(f'images/ship{n}.png') for n in range(1)]

    def __init__(self, game, settings, screen, sound, lasers=None):
        super().__init__()
        self.game = game
        self.screen = screen
        self.settings = settings
        self.sound = sound
        self.ships_left = settings.ship_limit  
        self.image = pg.image.load('images/ship0.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.posn = self.center_ship()    # posn is the centerx, bottom of the rect, not left, top
        self.vel = Vector()
        self.lasers = lasers
        self.shooting = False
        self.lasers_attempted = 0

        self.dying = self.dead = False

        self.timer_normal = Timer(image_list=self.ship_reg_image,is_loop=True)
        self.timer_explosion = Timer(image_list=self.ship_explosion_images, is_loop=False)
        self.timer = self.timer_normal

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)
    def reset(self): 
        self.vel = Vector()
        self.posn = self.center_ship()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y
    def die(self, sb, stats):
        if self.ships_left > 0:
            stats.ships_left -= 1
            self.ships_left -= 1

            if not self.dying:
                self.dying = True
                self.timer = self.timer_explosion 
                self.settings.alien_speed_factor=0
            self.game.reset()
            sb.prep_ships()
            print(f'Ship is dead! Only {self.ships_left} ships left')
        else:
            self.game.game_over()
            stats.game_active = False
            pg.mouse.set_visible(True)
            self.ships_left = 3
          
        
        
        # print(f'Ship is dead! Only {self.ships_left} ships left')
        # self.ships_left -= 1
        # print(f'Ship is dead! Only {self.ships_left} ships left')
        # self.game.reset() if self.ships_left > 0 else self.game.game_over()
    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            # self.kill()
            self.dying=False
            self.timer = self.timer_normal
            self.settings.alien_speed_factor=1
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(settings=self.settings, screen=self.screen,
                                ship=self, sound=self.sound)
        self.draw()
    def draw(self): 
        # pass
        # self.image = self.timer.image()
        # self.screen.blit(self.image, self.rect)
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
