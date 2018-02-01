# Steg 0 

Ladda ner startkod

Titta på strukturen

Öppna settings.py

# Steg 1

    def run(self):
        
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def new(self):
        # New game
        self.run()            


# Steg 2

    def events(self):
        for event in self.get_event():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

Prova att avsluta program.

# Steg 4

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_sprites()
        self.flip_display()

Prova att byta färg 

# Steg 5

    def update(self):

        # Game Loop - Update

        self.update_sprites()

# Steg 6

Öppna sprite sheet och titta på hur det ser ut inuti.

# Steg 7

    def load_data(self):

        self.spritesheet = SpriteSheet(self.image_path(SPRITESHEET))

    def __init__(self, title, width, height, fps):
        Game.__init__(self, title, width, height, fps)

        self.running = True

        self.load_data()

# Steg 8

Öppna sprites.py

    def load_images(self):
        self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
        self.image.set_colorkey(BLACK)

    class Player(GameSprite):
        def __init__(self, game):
            GameSprite.__init__(self, game, [game.all_sprites], layer=PLAYER_LAYER)

            self.load_images()
            
            self.rect = self.image.get_rect()
            self.rect.center = (40, HEIGHT - 100)        

Varför händer inget?

    def new(self):

        self.player = Player(self)

        self.run()
        
Prova ladda en annan bild

Placera Player någon annanstans.

# Steg 9

    def __init__(self, game):
        GameSprite.__init__(self, game, [game.all_sprites], layer=PLAYER_LAYER)

        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)

förklara vektorbegreppet och vec

    def update(self):

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -2
        if keys[pg.K_RIGHT]:
            self.vel.x = 2

        self.pos += self.vel

        self.rect.midbottom = self.pos
        
Varför händer inget nu??

    def update(self):

        # Game Loop - Update

        self.update_sprites()

Hur får vi gubben att stanna?

    def update(self):

        self.vel = vec(0, 0)        

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -2
        if keys[pg.K_RIGHT]:
            self.vel.x = 2

        self.pos += self.vel

        self.rect.midbottom = self.pos

# Steg 10

        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):

        self.acc = vec(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -0.5
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.5
            
        self.vel += self.acc            

        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
        
# Steg 10

Hur får vi gubben att inte försvinna?


    def update(self):

        ...

        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

# Steg 11

Hur får vi gubben att stanna av sig själv?

    def update(self):
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -0.5
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.5
            
        self.acc.x += self.vel.x * 0.01
