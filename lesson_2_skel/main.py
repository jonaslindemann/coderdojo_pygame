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
