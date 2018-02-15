import pygame as pg
from random import choice, randrange
from settings import *

from game import *

class Player(GameSprite):
    def __init__(self, game):
        GameSprite.__init__(self, game, [game.all_sprites], layer=PLAYER_LAYER)

        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()

        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)

        self.pos = vec(40, HEIGHT - 100)
        self.acc = vec(0, PLAYER_GRAV)
        self.friction = vec(PLAYER_FRICTION, 0)
        self.static = False

    def load_images(self):
        self.standing_frames =[self.game.spritesheet.get_image(614, 1063, 120, 191),
                               self.game.spritesheet.get_image(690, 406, 120, 201)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)


        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                              self.game.spritesheet.get_image(692, 1458, 120, 207)]

        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)

        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
        
    def jump(self):
        
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        if hits and not self.jumping:
            print("play sound")
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP_VEL

    def nothing_below(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        return len(hits)==0

    def update_sprite(self):
        
        self.animate()

        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            
    def update_position(self):
        self.rect.midbottom = self.pos           
        
             
        

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame+1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)
               
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
        
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)
                    
class Pow(GameSprite):
    def __init__(self, game, plat):
        GameSprite.__init__(self, game, [game.all_sprites, game.powerups], POW_LAYER)

        self.plat = plat
        self.type = choice(['boost'])

        self.image = self.game.spritesheet.get_image(820,1805,71,70)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5

        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(GameSprite):
    def __init__(self, game):
        GameSprite.__init__(self, game, [game.all_sprites, game.mobs], MOB_LAYER)

        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.image_down.set_colorkey(BLACK)

        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1

        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0

        self.dy = 0.5

    def update(self):

        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy>3 or self.vy <-3 :
            self.dy *= -1

        center = self.rect.center

        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.rect.y += self.vy

        self.mask = pg.mask.from_surface(self.image)

        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
        
class Cloud(GameSprite):
    def __init__(self, game):
        GameSprite.__init__(self, game, [game.all_sprites, game.clouds], CLOUD_LAYER)

        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50,101) / 100
        pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        self.vx = choice([-2,-1, 1, 2])

    def update(self):
        
        self.rect.x += self.vx

        # wrap around the sides of the screen

        if self.rect.left >= WIDTH:
            self.rect.right = 0 
        elif self.rect.right <= 0:
            self.rect.left = WIDTH

        if self.rect.top > HEIGHT * 2:
            self.kill()
        