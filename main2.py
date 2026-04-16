import pygame
import random

pygame.init()

# window
WIDTH, HEIGHT = 600, 400
BLOCK = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# text
def draw_text(text, color, x, y, size=25):
    font = pygame.font.SysFont("Arial", size)
    msg = font.render(text, True, color)
    screen.blit(msg, (x, y))

# food
def generate_food(snake):
    food_parts = []
    for i in range(10):
        while True:
            x = random.randrange(0, WIDTH, BLOCK)
            y = random.randrange(0, HEIGHT, BLOCK)
            if [x, y] not in snake and [x, y] not in food_parts:
                food_parts.append([x, y])
                break
    return food_parts

# reset_game
def reset_game():
    snake = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    food = generate_food(snake)
    score = 0
    level = 1
    speed = 6
    return snake, direction, food, score, level, speed

snake, direction, food, score, level, speed = reset_game()

game_over = False
game_close = False

# main
while not game_over:

    # window "game over"
    while game_close:
        screen.fill(WHITE)

        draw_text("You lost!", RED, 200, 140, 30)
        draw_text("Q - exit   C - restart", BLACK, 150, 200, 25)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False

                if event.key == pygame.K_c:
                    snake, direction, food, score, speed = reset_game()
                    game_close = False
        clock.tick(15)

    #  event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    
    
    keys = pygame.key.get_pressed()

    # Controls
    if keys[pygame.K_UP] and direction != "DOWN" or keys[pygame.K_w] and direction != "DOWN":
        direction = "UP"
    elif keys[pygame.K_DOWN] and direction != "UP" or keys[pygame.K_s] and direction != "UP":
        direction = "DOWN"
    elif keys[pygame.K_LEFT] and direction != "RIGHT" or keys[pygame.K_a] and direction != "RIGHT":
        direction = "LEFT"
    elif keys[pygame.K_RIGHT] and direction != "LEFT" or keys[pygame.K_d] and direction != "LEFT":
        direction = "RIGHT"

    # movement
    head = snake[0].copy()

    if direction == "UP":
        head[1] -= BLOCK
    if direction == "DOWN":
        head[1] += BLOCK
    if direction == "LEFT":
        head[0] -= BLOCK
    if direction == "RIGHT":
        head[0] += BLOCK

    # checking loss
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        game_close = True

    if head in snake:
        game_close = True

    snake.insert(0, head)

    # food
    if head in food:
        score += 1
        food.remove(head)

    if len(food) == 0:
        food = generate_food(snake)

    new_level = score // 3 + 1
    if new_level > level:
        level = new_level
        speed += 1 
    else:
        snake.pop()
    screen.fill(WHITE)

    # snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK, BLOCK))

    # food
    for part in food:
        pygame.draw.rect(screen, RED, (part[0], part[1], BLOCK, BLOCK))

    # text
    draw_text(f"Score: {score}", BLACK, 450, 10)
    draw_text(f"Level: {level}", BLACK, 250, 10)
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()