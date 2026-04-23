import pygame
from pygame.locals import *
import random

pygame.init()

# SCREEN SETTINGS
width = 300
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racer Game")

running = True


# PLAYER CAR
class player_car(pygame.sprite.Sprite):
    def __init__(self, path="images1.jpeg"):
        super().__init__()

        # load and scale player image
        imported_image = pygame.image.load(path)
        self.image = pygame.transform.scale(imported_image, (width//4, height//4))

        # define player position (bottom of the screen)
        self.rect = self.image.get_rect()
        self.rect.center = (47, 525)

    def move(self):
        # get pressed keys
        button = pygame.key.get_pressed()

        # move left and right
        if button[K_a]:
            self.rect.centerx -= 5
        elif button[K_d]:
            self.rect.centerx += 5

        # BOUNDARIES
        # prevent player from leaving the road
        if self.rect.centerx < 47:
            self.rect.centerx = 47
        if self.rect.centerx > 253:
            self.rect.centerx = 253


# ENEMY CAR
class red_car(pygame.sprite.Sprite):
    def __init__(self, path="pngtree-sedan-car-top-view-image-png-image_6558830.png"):
        super().__init__()

        # load and scale enemy image
        self.image = pygame.transform.scale(pygame.image.load(path), (width//4, height//4))

        # random starting position
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(47, 253)

        # score counter (points for avoiding enemy)
        self.score = 0

    def move(self, speed=10):
        # move enemy down
        self.rect.centery += speed

        # if enemy leaves screen → reset position
        if self.rect.centery > 675:
            self.rect.centery = -75
            self.rect.centerx = random.randint(47, 253)

            # increase score
            self.score += 10


# BACKGROUND 
class background:
    def __init__(self, path="images.jpeg"):
        imported_image = pygame.image.load(path)

        # scale background image
        self.image = pygame.transform.scale(imported_image, (width, height//2))

        # create 3 rectangles for scrolling effect
        rect1 = self.image.get_rect()
        rect2 = self.image.get_rect()
        rect3 = self.image.get_rect()

        rect2.centery += height//2
        rect3.centery += height

        self.rectangles = [rect1, rect2, rect3]

    def draw(self):
        # draw background images on screen
        for rectangle in self.rectangles:
            screen.blit(self.image, rectangle)

    def move(self):
        # move background down (scrolling road)
        for rectangle in self.rectangles:
            if rectangle.centery > 750:
                rectangle.centery = -150
            rectangle.centery += 3


# CREATE OBJECTS
bcg = background()
pc = player_car()
enemy = red_car()

# sprite groups
cars = pygame.sprite.Group()
cars.add(pc)
cars.add(enemy)

enemies = pygame.sprite.Group()
enemies.add(enemy)


#GAME LOOP
while running:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #DRAW BACKGROUND
    bcg.draw()
    bcg.move()

    #DRAW AND MOVE CARS
    for car in cars:
        screen.blit(car.image, car.rect)
        car.move()

    # ---------------- SCORE DISPLAY ----------------
    # show score at top-left corner
    font = pygame.font.SysFont("open dyslexic", 18)
    text = font.render("Score: " + str(enemy.score), True, (0, 0, 0))
    rect = text.get_rect()
    screen.blit(text, rect)

    #COLLISION DETECTION
    # check if player hits enemy
    if pygame.sprite.spritecollideany(pc, enemies):

        # fill screen with red color
        screen.fill((125, 20, 20))

        # show Game Over text
        go_font = pygame.font.SysFont("times new roman", 12)
        game_over_text = go_font.render(
            "Game Over! Your final score is: " + str(enemy.score),
            True,
            (20, 200, 200)
        )

        go_rect = game_over_text.get_rect()
        go_rect.center = (width//2, height//2)

        screen.blit(game_over_text, go_rect)
        pygame.display.update()

        # wait before closing
        pygame.time.delay(4000)

        running = False

    # FPS
    pygame.time.Clock().tick(60)

    # update screen
    pygame.display.flip()