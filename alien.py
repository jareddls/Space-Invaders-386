from tkinter import image_types
import pygame as pg
from pygame.sprite import Sprite, Group, GroupSingle
from laser import Lasers
from timer import Timer
from sound import Sound
from random import randint, choice
import wave
import os
import shutil


class Alien(Sprite):
    alien_images0 = [pg.image.load(f'images/alien0{n}.png') for n in range(2)]
    alien_images1 = [pg.image.load(f'images/alien1{n}.png') for n in range(2)]
    alien_images2 = [pg.image.load(f'images/alien2{n}.png') for n in range(2)]
    ufo_images = [pg.image.load(f'images/ufo{n}.png') for n in range(5)]
   
    alien_hitbox = pg.image.load(f'images/alien0.png')

    alien_timers = {'blue': Timer(image_list=alien_images0),
                    'orange': Timer(image_list=alien_images1), 
                    'purple': Timer(image_list=alien_images2),
                    'ufo': Timer(image_list=ufo_images)}    

    alien_explosion_images = [pg.image.load(f'images/explode{n}.png') for n in range(5)]
    ufo_explode_images = [pg.image.load(f'images/ufo_explosion{n}.png') for n in range(3)]

    def __init__(self, settings, screen, type, sound):
        super().__init__()
        self.sound = sound
        self.screen = screen
        self.settings = settings
        self.image = self.alien_hitbox
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        if self.type is self.alien_timers['blue']:
            self.value = self.settings.alien0_points
        elif self.type is self.alien_timers['orange']:
            self.value = self.settings.alien1_points
        elif self.type is self.alien_timers['purple']:
            self.value = self.settings.alien2_points
        # elif self.type is self.alien_timers['ufo']:
        #     self.value = self.settings.ufo_points
        
        self.dying = self.dead = False

        self.timer_normal = self.type
       
               
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, is_loop=False)  
        # self.ufo_timer_explosion = Timer(image_list=Alien.ufo_explode_images, is_loop=False)
        self.timer = self.timer_normal                                    

    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    def check_bottom_or_ship(self, ship): 
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= ship.rect.bottom or self.rect.colliderect(ship.rect)
    def hit(self):
        if not self.dying:
            self.dying = True 
            self.timer = self.timer_explosion

            self.sound.alien_death()
    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()
    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Aliens:
    increment = 0
    def __init__(self, game, screen, stats, sound, settings, lasers: Lasers, ship): 
        self.model_alien = Alien(settings=settings,sound=sound, screen=screen, type=type)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()

        self.ship_lasers = game.ship_lasers.lasers  
        self.aliens_lasers = game.alien_lasers  # a laser Group

        self.barriers = game.barriers

        # UFO Setup
        self.ufo = pg.sprite.GroupSingle()
        self.ufo_spawn_time = randint(1000, 1600)

        self.screen = screen
        self.stats = stats
        self.settings = settings
        self.ship = ship
        self.sound=sound
        self.shoot_requests = 0
        self.create_fleet()
    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 1 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x
    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (4 * alien_height) - ship_height)
        number_rows = int(available_space_y / (3.5 * alien_height))
        return number_rows        
    def reset(self):
        self.aliens.empty()
        self.create_fleet()
    def create_alien(self, alien_number, row_number, type):
        alien = Alien(settings=self.settings, screen=self.screen,type=type, sound=self.sound)
        alien_width = alien.rect.width

        alien.x = alien_width + 2 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number 
        self.aliens.add(alien)    

     
    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                if row_number == 0:
                    self.create_alien(alien_number, row_number + 3, Alien.alien_timers['purple'])
                elif row_number == 1 or row_number == 2:
                    self.create_alien(alien_number, row_number + 3, Alien.alien_timers['orange'])
                else: self.create_alien(alien_number, row_number + 3, Alien.alien_timers['blue'])

    def check_fleet_edges(self):
        for alien in self.aliens.sprites(): 
            if alien.check_edges():
                self.change_fleet_direction()
                break
    def check_fleet_bottom(self, sb, stats):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.die(sb, stats)
                self.increment = 0
                break
    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.increment = 0

            pg.mixer.music.stop()
            for filename in os.listdir('sounds'):
                file_path= os.path.join('sounds', filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            
            source = 'sounds/bg_song/bg_song0.wav'
            dst = 'sounds/bg_song0.wav'

            shutil.copy(source, dst)
            pg.mixer.music.load('sounds/bg_song0.wav')
            
            self.sound.play_bg()

            self.game.reset()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def check_collisions(self, sb, stats):  
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()

                CHANNELS = 1
                swidth = 2
                Change_RATE = 1.05

                spf = wave.open(f'sounds/bg_song{int(self.increment/10)}.wav', 'rb')
                RATE = spf.getframerate()
                signal = spf.readframes(-1)
                self.increment += 1

                if self.increment % 10 == 0:
                    

                    wf = wave.open(f'sounds/bg_song{int(self.increment/10)}.wav', 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(swidth)
                    wf.setframerate(RATE * Change_RATE)
                    wf.writeframes(signal)
                    wf.close()

                    pg.mixer.music.stop()
                    pg.mixer.music.load(f'sounds/bg_song{int(self.increment/10)}.wav')
                    self.sound.play_bg(fade_ms=0)

            self.sb.increment_score(alien.value)

        # if laser collide with barriers
        collisions = pg.sprite.groupcollide(self.barriers.barriers, self.ship_lasers, False, True)
        if collisions:
            for barriers in collisions:
                self.barriers.hit(barriers)
        
        collisions = pg.sprite.groupcollide(self.barriers.barriers, self.aliens_lasers.lasers, False, True)
        if collisions:
            for barriers in collisions:
                self.barriers.hit(barriers)

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.die(sb, stats)
            self.increment = 0
        
        collisions = pg.sprite.groupcollide(self.aliens_lasers.lasers, self.ship_lasers, True, True)

        collisions = pg.sprite.groupcollide(self.ufo, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                mystery_points = choice([50,100,150,200])
                ufo.hit(mystery_points)
                print(mystery_points)
                self.sb.increment_score(mystery_points)
            

    def update(self): 
        self.check_fleet_edges()
        self.check_fleet_bottom(self.sb, self.stats)
        self.check_collisions(self.sb, self.stats)
        self.check_fleet_empty()
        self.shoot_from_random_alien()

        self.ufo_timer()
        self.ufo.update()

        for alien in self.aliens.sprites():
            if alien.dead:   
                alien.remove()
            alien.update() 

    def draw(self): 
        for alien in self.aliens.sprites(): 
            alien.draw() 
    
    def ufo_timer(self):
        self.ufo_spawn_time -= 1
        # Will randomly spawn the UFO from the left or right of the screen
        if self.ufo_spawn_time <= 0:
            self.ufo.add(UFO(choice(['right', 'left']), self.game))
            self.sound.ufo()
            self.ufo_spawn_time = randint(1000, 1600)

class UFO(Sprite):
    # UFO image list
    ship_explosion_images = [pg.image.load(f'images/ship_explosion{n}.png') for n in range(13)]
    ufo_images = [pg.image.load(f'images/ufo{n}.png') for n in range(5)]

    fifty = [pg.image.load(f'images/fifty{n}.png') for n in range(2)]
    hundred = [pg.image.load(f'images/hundred{n}.png') for n in range(2)]
    hundredfifty = [pg.image.load(f'images/hundredfifty{n}.png') for n in range(2)]
    twohundred = [pg.image.load(f'images/twohundred{n}.png') for n in range(2)]

    

    def __init__(self, side, game):
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        self.timer_normal = Timer(image_list=self.ufo_images)
        self.timer = self.timer_normal

        self.dying = self.dead = False
        self.image = pg.image.load('images/ufo0.png')

        self.fifty_timer = Timer(image_list=self.fifty, delay=1500, is_loop=False)
        self.hundred_timer = Timer(image_list=self.hundred, delay=1500, is_loop=False)
        self.hundredfifty_timer = Timer(image_list=self.hundredfifty, delay=1500, is_loop=False)
        self.twohundred_timer = Timer(image_list=self.twohundred, delay=1500, is_loop=False)

        if side == 'right':
            x = self.settings.screen_width + 50
            self.speed = -1
        else:
            x = -50
            self.speed = 1

        self.rect = self.image.get_rect(topleft=(x, 110))

    def update(self):
        self.rect.x += self.speed

        if (self.timer == self.fifty_timer 
            or self.timer == self.hundred_timer
            or self.timer == self.hundredfifty_timer
            or self.timer == self.twohundred_timer) and self.timer.is_expired():
            self.kill()

        self.draw()

    def hit(self, points):
        if not self.dying:
            self.dying = True
            self.points = points
            print(self.points)
            if self.points == 50:
                self.timer = self.fifty_timer

            elif self.points == 100:
                self.timer = self.hundred_timer

            elif self.points == 150:
                self.timer = self.hundredfifty_timer

            elif self.points == 200:
                self.timer = self.twohundred_timer


    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
