import sys
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
        ship.image = pg.image.load('images/ship1.png')
    elif key in movement.keys():
        # if key is pg.K_LEFT and not pg.K_RIGHT:
        #     ship.vel = settings.ship_speed_factor * movement[key]
        # elif key is pg.K_RIGHT and not pg.K_LEFT:
        ship.vel += settings.ship_speed_factor * movement[key]

def check_keyup_events(event, settings, ship):
    key = event.key
    if key == pg.K_SPACE: 
        ship.shooting = False
        ship.image = pg.image.load('images/ship0.png')
    elif key == pg.K_ESCAPE:
        ship.vel = Vector()
    elif key in movement.keys(): 
        ship.vel -= settings.ship_speed_factor * movement[key]
    # elif key in movement.keys(): ship.vel = Vector()

def check_events(settings, ship):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN: 
            check_keydown_events(event=event, settings=settings, ship=ship)
        elif event.type == pg.KEYUP: 
            check_keyup_events(event=event, settings = settings, ship=ship)

def clamp(posn, rect, settings):
    left, top = posn.x, posn.y
    width, height = rect.width, rect.height
    left = max(0, min(left, settings.screen_width - width))
    top = 700
    return Vector(x=left, y=top), pg.Rect(left, top, width, height)
