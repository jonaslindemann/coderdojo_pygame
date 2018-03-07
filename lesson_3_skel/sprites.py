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
        self.acc = vec(0, 0)
        self.friction = vec(-0.12, 0)
        self.static = False
               
    def load_images(self):
        self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
        self.image.set_colorkey(BLACK)
        
    def update_sprite(self):
        keys = pg.key.get_pressed()
        
        self.acc.x = 0.0
        self.acc.y = 0.8
    
        if keys[pg.K_LEFT]:
            self.acc.x = -0.2
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.2
    
    def update_position(self):
        self.rect.midbottom = self.pos           

class Platform(GameSprite):
    def __init__(self, game, x, y):
        GameSprite.__init__(self, game, [game.all_sprites, game.platforms], PLATFORM_LAYER)

        self.images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                       self.game.spritesheet.get_image(213, 1662, 201, 100)]
        
        self.image = choice(self.images)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
