import pygame as pg
from random import choice, randrange
from settings import *
vec = pg.math.Vector2

from game import *

class Player(GameSprite):
    def __init__(self, game):
        GameSprite.__init__(self, game, [game.all_sprites], layer=PLAYER_LAYER)

        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
        self.image.set_colorkey(BLACK)
        
    def update(self):

        # self.acc = vec(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction

        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion

        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        
        self.pos += self.vel + 0.5 * self.acc

        # wrap around the sides of the screen

        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
               
        