import pygame as pg
import time
from laser import LaserType

class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.2)
        alien_laser_sound = pg.mixer.Sound('sounds/important/alien_laser.wav')
        laser_sound = pg.mixer.Sound('sounds/important/laser.wav')
        alien_death_sound = pg.mixer.Sound('sounds/important/alien_death.wav')
        ship_death_sound = pg.mixer.Sound('sounds/important/ship_death.wav')
        gameover_sound = pg.mixer.Sound('sounds/important/gameover.wav')
        ufo_sound = pg.mixer.Sound('sounds/important/ufo.wav')
        self.sounds = {'alienlaser': alien_laser_sound, 'laser': laser_sound, 'gameover': gameover_sound, 'alien_death':alien_death_sound, 'ship_death':ship_death_sound, 'ufo_sound':ufo_sound }

    def play_bg(self, loop=-1, start=0, fade_ms=3000):
        pg.mixer.music.play(loop, start, fade_ms)

    def stop_bg(self):
        pg.mixer.music.stop()  

    def alien_death(self):
        pg.mixer.Sound.play(self.sounds['alien_death'])
        pg.mixer.Sound.set_volume(self.sounds['alien_death'], 0.1)

    def ship_death(self):
        pg.mixer.Sound.play(self.sounds['ship_death'])
        pg.mixer.Sound.set_volume(self.sounds['ship_death'], 0.1)

    def ufo(self):
        pg.mixer.Sound.play(self.sounds['ufo_sound'])


    def shoot_laser(self, type): 
        # pg.mixer.Sound.play(self.sounds['laser'])
        
        pg.mixer.Sound.play(self.sounds['alienlaser' if type == LaserType.ALIEN else 'laser'])
        pg.mixer.Sound.set_volume(self.sounds['laser'], 0.1)
        pg.mixer.Sound.set_volume(self.sounds['alienlaser'], 0.1)
    def gameover(self): 
        self.stop_bg() 
        pg.mixer.music.load('sounds/important/gameover.wav')
        self.play_bg(0,0,0)
        time.sleep(2.5)
        pg.mixer.music.load('sounds/important/start_song.wav')
        self.play_bg()
