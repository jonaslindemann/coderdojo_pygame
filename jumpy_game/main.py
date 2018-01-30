import pygame as pg
import random

from settings import *
from sprites import *
from game import *

class JumpyGame(Game):
    def __init__(self, title, width, height, fps):
        Game.__init__(self, title, width, height, fps)

        self.running = True
        self.font_name = self.match_font(FONT_NAME)

        self.load_data()

    def load_data(self):

        try:
            with open(path.join(self.dir, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0

        self.spritesheet = SpriteSheet(self.image_path(SPRITESHEET))

        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(self.load_image('cloud{}.png'.format(i)).convert())

        self.jump_sound = self.load_sound("Jump33.wav")
        self.boost_sound = self.load_sound("Boost16.wav")

    def new(self):

        self.score = 0
        
        self.platforms = self.create_sprite_group()
        self.powerups = self.create_sprite_group()
        self.mobs = self.create_sprite_group()
        self.clouds = self.create_sprite_group()

        self.player = Player(self)
        
        for plat in PLATFORM_LIST:
            Platform(self, plat[0], plat[1])

        self.mob_timer = 0

        self.load_music("Happy Tune.ogg")

        for i in range(10):
            c = Cloud(self)
            c.rect.y += 500 
        
        self.run()
        
    def run(self):
        
        self.play_music()
        
        self.playing = True
        
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

        # check if player hits a platform - only if falling

        if self.player.vel.y > 0:
            hits = self.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = max(hits, key = lambda x: x.rect.bottom)

                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:

                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # if player reaches top 1/4 of screen

        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 15:
                Cloud(self)
            
            self.player.pos.y += max(abs(self.player.vel.y), 2)

            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)

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

        # spawn new platforms to keep same average number
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
        
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
        self.draw_text("Highscore: "+ str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        
        self.flip_display()
        self.wait_for_key()
        
        self.fadeout_music(500)
    
    def show_game_over_screen(self):

        if not self.running:
            return

        self.load_music("Yippee.ogg")
        self.play_music()

        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(self.game_path(HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore: "+ str(self.highscore), 22, WHITE, WIDTH / 2, 15)
            
        self.flip_display()
        self.wait_for_key()

        self.fadeout_music(500)

g = JumpyGame(TITLE, WIDTH, HEIGHT, FPS)

g.show_start_screen()

while g.running:
    g.new()
    g.show_game_over_screen()
    
g.quit()
