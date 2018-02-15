# Step 1

Lägg till 

        self.pos = vec(40, HEIGHT - 100)
        self.acc = vec(0, 0)
        self.friction = vec(0, 0)
        self.static = False

if Player Sprite

# Steg 2

Lägg till en update_sprite() och en update_position funktion till Player

    def update_sprite(self):
        pass
    
    def update_position(self):
        self.rect.midbottom = self.pos

# Steg 3

Flytta spelaren med tangenterna

        keys = pg.key.get_pressed()
    
        if keys[pg.K_LEFT]:
            self.vel.x = -5
        if keys[pg.K_RIGHT]:
            self.vel.x = 5

# Steg 4

Använda acceleration

    def update_sprite(self):
        keys = pg.key.get_pressed()
    
        if keys[pg.K_LEFT]:
            self.acc.x = -0.2
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.2

vad händer?

# Steg 5

Använda acceleration

    def update_sprite(self):
        keys = pg.key.get_pressed()
        
        self.acc.x = 0.0
    
        if keys[pg.K_LEFT]:
            self.acc.x = -0.2
        if keys[pg.K_RIGHT]:
            self.acc.x = 0.2
            
# Steg 6

    self.friction = vec(-0.12, 0)


# Steg 7 plattformar

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
