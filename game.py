import pygame, sys, random

print("It runs!")

pygame.init()

size = (width, height) = 500, 500
screen = pygame.display.set_mode(size)

speed = [0, 0]

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load("./cat.svg")
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)

        self.total_lives = 5
        self.last_hit = 0

    def update(self):
        self.last_hit = pygame.time.get_ticks()
        self.total_lives -= 1 

        if self.total_lives <= 0:
            print("Game over!")
            sys.exit()

class Corona(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./germ.svg")
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 500), random.randint(0, 500))
        self.speed = [3, 3]

    def update(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] =  -self.speed[0] * 1.5
            self.speed[1] = self.speed[1] * random.uniform(0.5, 1.1)
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1] * 1.5
            self.speed[0] = self.speed[0] * random.uniform(0.5, 1.1)

        if self.speed[0] > 6:
            self.speed[0] -= 0.5
        if self.speed[0] < -6:
            self.speed[0] += 0.5

        if self.speed[1] > 6:
            self.speed[1] -= 0.5
        if self.speed[1] < -6:
            self.speed[1] += 0.5


main = MainCharacter()
main_sprite = pygame.sprite.Group()
main_sprite.add(main)

bad_sprites = pygame.sprite.Group()
for _ in range(3):
    bad_sprites.add(Corona())

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill((0, 0, 0))
    
    main_sprite.draw(screen)
    bad_sprites.draw(screen)

    key = pygame.key.get_pressed()

    if key[pygame.K_a] and speed[0] > -20:
        speed[0] -= 1.5
    if key[pygame.K_d] and speed[0] < 20:
        speed[0] += 1.5
    if key[pygame.K_w] and speed[1] > -20:
        speed[1] -= 1.5 
    if key[pygame.K_s] and speed[1] < 20:
        speed[1] += 1.5 

    if main.rect.left < 0 or main.rect.right > width:
        speed[0] =  -speed[0] * 1.5
    if main.rect.top < 0 or main.rect.bottom > height:
        speed[1] = -speed[1] * 1.5

    if speed[0] > 0:
        speed[0] -= 0.5
    if speed[0] < 0:
        speed[0] += 0.5

    if speed[1] > 0:
        speed[1] -= 0.5
    if speed[1] < 0:
        speed[1] += 0.5
    
    main.rect = main.rect.move(speed)
    bad_sprites.update()

    myFont = pygame.font.SysFont("Times New Roman", 18)
    numLivesDraw = myFont.render(f"{main.total_lives} remaining", 1, (250, 250, 250))
    screen.blit(numLivesDraw, (30, 30))

    collisions = pygame.sprite.spritecollideany(main, bad_sprites) 
    if collisions != None:
        interval = pygame.time.get_ticks() - main.last_hit 
        if interval > 1000: # one second 
            main_sprite.update()

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()