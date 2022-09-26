import pygame as pg 
import pickle
from pygame.sprite import Group
from ship import Ship
import game_functions as gf
# import pygame.font

class Scoreboard:
    def __init__(self, game, stats, sound): 
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = stats
        self.sound = sound

        self.text_color = (255, 255, 255)
        self.font = pg.font.Font('font/pixel.ttf', 24)
        self.score_image = None 
        self.score_rect = None

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def increment_score(self, type): 
        # self.score += self.settings.alien0_points
        self.score += type
        self.prep_score()
        # gf.check_high_score(stats, sb)

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 50

        self.score_title = self.font.render('SCORE', True, self.text_color, self.settings.bg_color)
        self.score_title_rect = self.score_title.get_rect()
        self.score_title_rect.right = self.screen_rect.right - 20
        self.score_title_rect.top = 15
        

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 20
        self.high_score_rect.top = 50

        self.hs_title = self.font.render('HI-SCORE', True, self.text_color, self.settings.bg_color)
        self.hs_title_rect = self.hs_title.get_rect()
        self.hs_title_rect.left = self.screen_rect.left + 20
        self.hs_title_rect.top = 15

    def list_high_scores(self):
        self.screen.blit(pg.image.load(f'images/space_bg.png'), (0,0))
        
        with open('scores/hs_list.dat', 'rb') as highscores:
            list_hs1 = pickle.load(highscores)
            list_hs2 = pickle.load(highscores)
            list_hs3 = pickle.load(highscores)
            list_hs4 = pickle.load(highscores)
            list_hs5 = pickle.load(highscores)
            print(list_hs1)
        self.list_hs_image = self.font.render(str(f'{list_hs1[0]} : {list_hs1[1]}'), True,
            self.text_color, self.settings.bg_color)
        self.list_hs_rect = self.list_hs_image.get_rect()
        self.list_hs_rect.center = self.screen_rect.center


    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(f'Level: {self.stats.level}'), True,
            self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.bottom = self.score_rect.bottom + 710

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(game=self.game, settings=self.settings, screen=self.screen,sound=self.sound)
            ship.rect.x = 10 + ship_number * (ship.rect.width * 1.5)
            ship.rect.y = 750
            self.ships.add(ship)

    def prep_pt_table(self):
        """Show the table"""
        self.score_table_text = self.font.render('* SCORE ADVANCE TABLE *', True, (255,255,255), (0,0,0))
        self.score_table_text_rect = self.score_table_text.get_rect()
        self.score_table_text_rect.center =  self.screen_rect.center

        self.first_alien_pts_text = self.font.render('= 050 POINTS', True, (255,255,255), (0,0,0))
        self.first_alien_pts_text_rect = self.first_alien_pts_text.get_rect()
        self.first_alien_pts_text_rect =  (255, 650)

        self.second_alien_pts_text = self.font.render('= 100 POINTS', True, (255,255,255), (0,0,0))
        self.second_alien_pts_text_rect = self.second_alien_pts_text.get_rect()
        self.second_alien_pts_text_rect = (255, 590)

        self.third_alien_pts_text = self.font.render('= 150 POINTS', True, (255,255,255), (0,0,0))
        self.third_alien_pts_text_rect = self.third_alien_pts_text.get_rect()
        self.third_alien_pts_text_rect = (255, 530)

        self.ufo_pts_text = self.font.render('= ??? POINTS', True, (255,255,255), (0,0,0))
        self.ufo_pts_text_rect = self.ufo_pts_text.get_rect()
        self.ufo_pts_text_rect = (255, 470)

    def reset(self): 
        self.score = 0
        self.level = 1
        self.update_score()
        # self.update_level()
        # self.update_ships()

    def update_score(self): 
        self.draw_score()

    def update_hs(self): 
        self.draw_hs()

    def update_level(self): 
        self.draw_level()

    def update_ships(self):
        self.draw_ships() 

    def draw_score(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_title, self.score_title_rect)
    
    def draw_hs(self):
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.hs_title, self.hs_title_rect)
    
    def draw_level(self):
        self.screen.blit(self.level_image, self.level_rect)
    
    def draw_ships(self):
        self.ships.draw(self.screen)

    def update_list_hs(self):
        self.draw_list_hs()

    def draw_list_hs(self):
        self.screen.blit(self.list_hs_image, self.list_hs_rect)

    def update_pt_table(self):
        self.draw_pt_table()

    def draw_pt_table(self):
        self.screen.blit(pg.image.load('images/alien0.png'), (195, 645))
        self.screen.blit(pg.image.load('images/alien10.png'), (195, 585))
        self.screen.blit(pg.image.load('images/alien20.png'), (195, 525))
        self.screen.blit(pg.image.load('images/ufo0.png'), (178, 465))

        self.screen.blit(self.first_alien_pts_text, self.first_alien_pts_text_rect)
        self.screen.blit(self.second_alien_pts_text, self.second_alien_pts_text_rect)
        self.screen.blit(self.third_alien_pts_text, self.third_alien_pts_text_rect)
        self.screen.blit(self.ufo_pts_text, self.ufo_pts_text_rect)

        self.screen.blit(self.score_table_text, self.score_table_text_rect)