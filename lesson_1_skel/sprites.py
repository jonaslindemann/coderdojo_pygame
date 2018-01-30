import pygame as pg
from random import choice, randrange
from settings import *
vec = pg.math.Vector2

from game import *

class Player(GameSprite):
    def __init__(self, game):
        GameSprite.__init__(self, game, [game.all_sprites], layer=PLAYER_LAYER)
                