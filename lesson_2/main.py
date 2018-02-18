import pygame as pg
import random

from settings import *
from sprites import *
from game import *

class JumpyGame(Game):
    def __init__(self, title, width, height, fps):
        Game.__init__(self, title, width, height, fps)

        self.running = True

        self.load_data()

    def load_data(self):

        self.spritesheet = SpriteSheet(self.image_path(SPRITESHEET))

    def new(self):
        
        self.init_sprites()
        
        self.platforms = self.create_sprite_group()
        
        for plat in PLATFORM_LIST:
            Platform(self, plat[0], plat[1])

        self.player = Player(self)
        self.run()
        
    def run(self):
        
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        # Game Loop - Update

        self.update_sprites()
        
        if self.player.vel.y > 0:
            hits = self.spritecollide(self.player, self.platforms, False)
            if hits:
                
                max_x = 0
                lowest = None
                
                for sprite in hits:
                    if sprite.rect.bottom > max_x:
                        max_x = sprite.rect.bottom
                        lowest = sprite
                
                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:

                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
        

    def events(self):
        for event in self.get_event():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
       
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_sprites()
        self.flip_display()
        
    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass
          
g = JumpyGame(TITLE, WIDTH, HEIGHT, FPS)

g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()
    
g.quit()
