import wave
import pygame as pg
from timer import Timer
from settings import Settings
import game_functions as gf

from laser import Lasers
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button
import sys


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_icon(pg.image.load(f'images/ufo0.png'))
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Space Invaders")

        self.sound = Sound(bg_music="sounds/start_song.wav")

        self.stats = GameStats(settings=self.settings)
        self.scoreboard = Scoreboard(game=self, stats=self.stats, sound=self.sound)  
        self.lasers = Lasers(settings=self.settings)
        self.ship = Ship(game=self, screen=self.screen, settings=self.settings, stats=self.stats, sound=self.sound, lasers=self.lasers)
        self.aliens = Aliens(game=self, screen=self.screen, stats=self.stats, sound=self.sound, settings=self.settings, lasers=self.lasers, ship=self.ship)
        self.play_button = Button(self.settings, self.screen, "PLAY", 350, 750, 24)

        self.settings.initialize_speed_settings()
       

    def reset(self):
        print('Resetting game...')
        self.lasers.reset()
        self.ship.reset()
        self.aliens.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        self.stats.game_active = False

    def play(self):
        self.sound.play_bg()

        while True: 
            gf.check_events(settings=self.settings, sound=self.sound, ship=self.ship, stats=self.stats, sb=self.scoreboard, play_button=self.play_button,screen=self.screen,aliens=self.aliens,lasers=self.lasers)

            if self.stats.game_active:
                self.screen.blit(pg.image.load('images/space_bg.png'), (0,0))

                self.ship.update()
                self.aliens.update()
                self.lasers.update()

                self.scoreboard.update_score()
                
                self.scoreboard.update_level()
                self.scoreboard.update_ships()

                self.scoreboard.prep_ships()
                self.scoreboard.update_hs()
                
                gf.check_high_score(stats=self.stats, sb=self.scoreboard)
                self.scoreboard.prep_high_score()

                pg.draw.line(self.screen, (255, 255, 255), (0, 85), (800, 85), 3)
                pg.draw.line(self.screen, (255, 255, 255), (0,735), (800, 735), 3)
            else: 
                self.screen.blit(self.settings.bg, (0,0))
                self.play_button.update()
                self.scoreboard.reset()

                gf.check_high_score(stats=self.stats, sb=self.scoreboard)
                self.scoreboard.update_hs()

                self.scoreboard.prep_score()
                self.scoreboard.prep_ships()
                self.scoreboard.prep_level()
                self.scoreboard.prep_pt_table()
                self.scoreboard.update_pt_table()
                self.stats.reset_stats()
                

            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
