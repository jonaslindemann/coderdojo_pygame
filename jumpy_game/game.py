import pygame as pg
import random
from os import path
vec = pg.math.Vector2
from settings import *


class GameSprite(pg.sprite.Sprite):
    def __init__(self, game, groups, layer=999):
        self.groups = groups
        self._layer = layer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.friction = vec(0,0)
        self.static = True
        
    def update(self):
        
        self.update_sprite()
        
        if not self.static:

            # apply friction

            self.acc.x += self.vel.x * self.friction.x
            self.acc.y += self.vel.y * self.friction.y

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
                
            self.update_position()
            
    def update_sprite(self):
        pass
        
    def update_position(self):
        self.rect.midbottom = self.pos
    
    def animate(self):
        pass
        
        

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        return image

class Game:
    def __init__(self, title, width, height, fps):
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)

        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')
        self.clock = pg.time.Clock()
        self.fps = fps
        
        self.init_sprites()
        
    def init_sprites(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        
    def create_sprite_group(self):
        return pg.sprite.Group()
    
    def update_sprites(self):
        self.all_sprites.update()
        
    def spritecollide(self, sprite, group, dokill, collided = None):
        return pg.sprite.spritecollide(sprite, group, dokill, collided)
    
    def draw_sprites(self):
        self.all_sprites.draw(self.screen)
        
    def get_event(self):
        return pg.event.get()

    def match_font(self, name):
        return pg.font.match_font(name)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def game_path(self, filename):
        return self.dir

    def image_path(self, filename):
        return path.join(self.img_dir, filename)

    def sound_path(self, filename):
        return path.join(self.snd_dir, filename)

    def load_sound(self, filename):
        return pg.mixer.Sound(self.sound_path(filename))

    def load_image(self, filename):
        return pg.image.load(self.image_path(filename))

    def load_music(self, filename):
        pg.mixer.music.load(self.sound_path(filename))

    def play_music(self):
        pg.mixer.music.play(loops=-1)

    def fadeout_music(self, fadeout_time):
        pg.mixer.music.fadeout(fadeout_time)

    def get_ticks(self):
        return pg.time.get_ticks()

    def flip_display(self):
        pg.display.flip()

    def quit(self):
        pg.quit()


