import sys
import pickle
from collections import OrderedDict
import pygame as pg
from vector import Vector

movement = {pg.K_LEFT: Vector(-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_RIGHT: Vector(1, 0),
            pg.K_UP: Vector(0, -1),
            pg.K_DOWN: Vector(0, 1)
            }

  
def check_keydown_events(event, settings, ship):
    key = event.key
    if key == pg.K_SPACE: 
        ship.shooting = True
    elif key in movement.keys():
        ship.vel += settings.ship_speed_factor * movement[key]

def check_keyup_events(event, settings, ship):
    key = event.key
    if key == pg.K_SPACE: 
        ship.shooting = False
    elif key == pg.K_ESCAPE:
        ship.vel = Vector()
    elif key in movement.keys(): 
        ship.vel -= settings.ship_speed_factor * movement[key]

def check_events(settings, sound, screen, stats, sb, play_button, ship, aliens, lasers):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN: 
            check_keydown_events(event=event, settings=settings, ship=ship)
        elif event.type == pg.KEYUP: 
            check_keyup_events(event=event, settings = settings, ship=ship)
        elif event.type == pg.MOUSEBUTTONUP:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(settings, sound, screen, stats, sb, play_button, ship, aliens, lasers, mouse_x, mouse_y)

def check_play_button(settings, sound, screen, stats, sb, play_button, ship, aliens, lasers, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pg.mouse.set_visible(False)

        stats.game_active = True

        aliens.reset()
        lasers.reset()
        
        sb.prep_score()
        sb.reset()

        ship.center_ship()
        pg.mixer.music.load('sounds/bg_song.wav')
        sound.play_bg()
        

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if sb.score > stats.high_score:
        stats.high_score = sb.score
        with open('scores/high_scores.dat', 'wb') as file:
            pickle.dump(stats.high_score, file)
        sb.prep_high_score()
        

def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = 700
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)
