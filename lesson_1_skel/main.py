import pygame as pg
import random

from settings import *
from sprites import *
from game import *

class JumpyGame(Game):
    def __init__(self, title, width, height, fps):
        Game.__init__(self, title, width, height, fps)

        self.running = True

    def new(self):
        # New game
        pass
       
    def run(self):
        # Game loop
        pass
    
    def update(self):
        # Game loop - Update
        pass

    def events(self):
        # Game loop - Events
        pass
       
    def draw(self):
        # Game loop - Draw
        pass

    def show_start_screen(self):
        # Show start screen
        pass
    
    def show_go_screen(self):
        # Show Game Over screen
        pass
          
g = JumpyGame(TITLE, WIDTH, HEIGHT, FPS)

g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()
    
g.quit()
