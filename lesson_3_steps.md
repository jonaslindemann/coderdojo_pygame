# Hopp

settings.py:

    PLAYER_JUMP_VEL = 20

sprites.py

    def jump(self):
        
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP_VEL

main.py:

    def events(self):
        for event in self.get_event():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def update(self):

                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
    

# Game over

    def update(self):

        # Die! 
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

# Ljud

main.py:

    def load_data(self):

        self.jump_sound = self.load_sound("Jump33.wav")
    
sprites.py:

    def jump(self):

        if hits and not self.jumping:
            print("play sound")
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP_VEL

# Fortsättning uppåt

main.py:

    def update(self):

        if self.player.rect.top <= HEIGHT / 4:
            
            self.player.pos.y += max(abs(self.player.vel.y), 2)
           
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

Vad händer????

# Skapa fler plattformar

    def update(self):

        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))            
    
# Poängräkning

main.py:

    def new(self):

        self.score = 0


    def update(self):

            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

settings.py:

FONT_NAME = "arial"

maint.py:

    def __init__:
        self.font_name = self.match_font(FONT_NAME)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_sprites()
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        self.flip_display()

# Bakgrundsmusik

    def new(self):

        self.load_music("Happy Tune.ogg")
    
    def run(self):

        self.play_music()

        ...


        self.fadeout_music(500)


