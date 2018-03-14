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
        
        self.font_name = self.match_font(FONT_NAME)
        

    def load_data(self):

        self.spritesheet = SpriteSheet(self.image_path(SPRITESHEET))
        
        self.jump_sound = self.load_sound("Jump33.wav")
        self.boost_sound = self.load_sound("Boost16.wav")

    def new(self):
        
        self.score = 0
        
        self.init_sprites()
        
        self.platforms = self.create_sprite_group()
        self.powerups = self.create_sprite_group()
        self.mobs = self.create_sprite_group()
        self.mob_timer = 0
        
        for plat in PLATFORM_LIST:
            Platform(self, plat[0], plat[1])

        self.player = Player(self)
        
        self.load_music("Happy Tune.ogg")
        
        self.run()
        
    def run(self):
        
        self.playing = True
        
        self.play_music()
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
        self.fadeout_music(500)

    def update(self):

        # Game Loop - Update

        self.update_sprites()
        
        # Spawn a mob

        now = self.get_ticks()
        
        if now - self.mob_timer > MOB_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
            
        # hit mobs

        mob_hits = self.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False            
        
        # Check platform
        
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
                        self.player.jumping = False
                        
        # Top of screen
                        
        if self.player.rect.top <= HEIGHT / 4:
            
            self.player.pos.y += max(abs(self.player.vel.y), 2)
           
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
                    
        # Powerup
                    
        pow_hits = self.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()                
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False                        
                        
        # Die!
        
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False
            
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))            
            


    def events(self):
        for event in self.get_event():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                
       
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_sprites()
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)        
        self.flip_display()
        
    def show_start_screen(self):
        self.load_music("Yippee.ogg")
        self.play_music()

        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        
        self.flip_display()
        self.wait_for_key()
        
        self.fadeout_music(500)
    
    def show_go_screen(self):

        if not self.running:
            return

        self.load_music("Yippee.ogg")
        self.play_music()

        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            
        self.flip_display()
        self.wait_for_key()

        self.fadeout_music(500)

          
g = JumpyGame(TITLE, WIDTH, HEIGHT, FPS)

g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()
    
g.quit()
