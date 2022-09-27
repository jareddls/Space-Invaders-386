import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint
from timer import Timer

class Laser(Sprite):
    """A class to manage lasers fired from the ship"""

    laser_images = [pg.image.load(f'images/laser{n}.png') for n in range (2)]
    laser_timer = Timer(image_list=laser_images)

    def __init__(self, settings, screen, ship, sound):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load('images/laser0.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        self.speed_factor = settings.laser_speed_factor

        self.timer_normal = Timer(image_list=self.laser_images)
        self.timer = self.timer_normal
        sound.shoot_laser()
    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

class Lasers:
    def __init__(self, settings):
        self.lasers = Group()
        self.settings = settings
    def reset(self):
        self.lasers.empty()        
    def shoot(self, settings, screen, ship, sound):
        self.lasers.add(Laser(settings=settings, screen=screen, ship=ship, sound=sound))
    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.top <= 85: self.lasers.remove(laser)
    def draw(self):
        for laser in self.lasers.sprites(): laser.draw()

