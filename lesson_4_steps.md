# Animering

https://board.net/p/CoderDojoSkurup

Först måste vi ladda bilder som vi skall använda till animeringen:

class Player(GameSprite):
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

## Animeringsfunktion

class Player(GameSprite):

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

För att få igång animeringen:
                    
        def update_sprite(self):
            
            self.animate()

# Powerups

Först skall vi skapa en ny Sprite:

## Ny sprite

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

## Ny sprite-grupp:

    def new(self):

        self.score = 0
        
        self.init_sprites()
        
        self.platforms = self.create_sprite_group()
        self.powerups = self.create_sprite_group()

## Skapa powerups

Powerups skall skapas på plattformarna, så vi behöver något som skapar dessa:

Först behöver vi lite variabler i settings.py:

# Game properties

BOOST_POWER = 60
POW_SPAWN_PCT = 20

## Skapa powerup på plattform

class Platform(GameSprite):
    def __init__(self, game, x, y):

        ...

        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

Prova och kör...

## Aktivera powerups

main.py:

    def update(self):

        ...

        # Powerup

        pow_hits = self.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

## Ljud för power up

Hur skall vi åstadkomma detta?

main.py:

    def load_data(self):

        self.boost_sound = self.load_sound("Boost16.wav")

Lägg in ljudet precis som vi gjorde för jump

# Startup skärm

main.py:

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

# Game over skärm

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

# Monster

## Sprite

sprites.py:

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

## Sprite grupp

main.py:

    def new(self):

        self.score = 0
        
        self.init_sprites()
        
        self.platforms = self.create_sprite_group()
        self.powerups = self.create_sprite_group()
        self.mobs = self.create_sprite_group()
        self.mob_timer = 0
        

## Inställnings variabel

settings.py

# Game properties

BOOST_POWER = 60
POW_SPAWN_PCT = 20
MOB_FREQ = 5000


## Skapa monster

main.py

    def update(self):

        # Spawn a mob

        now = self.get_ticks()
        
        if now - self.mob_timer > MOB_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

Funkar det? Vi måste också kontrollera om den träffar oss:

    def update(self):

        # hit mobs

        mob_hits = self.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

Ljud till monster?




