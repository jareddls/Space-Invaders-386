import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from timer import Timer
from enum import Enum

class LaserType(Enum):
    ALIEN = 1 
    SHIP = 2

class Laser(Sprite):
    """A class to manage lasers fired from the ship"""

    alien_laser_images = [pg.image.load(f'images/alien_laser{n}.png') for n in range (2)]
    ship_laser_images = [pg.image.load(f'images/laser{n}.png') for n in range (2)]

    laser_images = {LaserType.ALIEN: alien_laser_images, LaserType.SHIP: ship_laser_images}
    # laser_timer = Timer(image_list=laser_images)

    def __init__(self, settings, screen, x, y, sound, type):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load('images/laser0.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.y = float(self.rect.y)
        self.type = type
        self.speed_factor = settings.laser_speed_factor
        imagelist = Laser.laser_images[type]
        self.timer = Timer(image_list=imagelist, delay=200)


        # self.timer_normal = Timer(image_list=self.laser_images)
        # self.timer = self.timer_normal
        sound.shoot_laser(type=self.type)
    def update(self):
        self.y += self.speed_factor if self.type == LaserType.ALIEN else -self.speed_factor
        self.rect.y = self.y
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

class Lasers:
    def __init__(self, settings, type):
        self.lasers = Group()
        self.settings = settings
        self.type = type
    def reset(self):
        self.lasers.empty()        
    def shoot(self, game, x, y):
        self.lasers.add(Laser(settings=game.settings, screen=game.screen, x=x, y=y, sound=game.sound, type=self.type))
    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.top <= 85: self.lasers.remove(laser)
    def draw(self):
        for laser in self.lasers.sprites(): laser.draw()

