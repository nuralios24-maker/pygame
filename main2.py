import pygame
import random

pygame.init()

# window
WIDTH, HEIGHT = 600, 400
BLOCK = 10

image21 = pygame.image.load('6a68c9aee6a3655.png')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# colors
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

# reset
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

# main loop
while not game_over:

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # controls
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and direction != "DOWN":
        direction = "UP"
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and direction != "UP":
        direction = "DOWN"
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and direction != "RIGHT":
        direction = "LEFT"
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and direction != "LEFT":
        direction = "RIGHT"

    # move head
    head = snake[0].copy()

    if direction == "UP":
        head[1] -= BLOCK
    elif direction == "DOWN":
        head[1] += BLOCK
    elif direction == "LEFT":
        head[0] -= BLOCK
    elif direction == "RIGHT":
        head[0] += BLOCK

    # wall collision (ВАЖНО: СЮДА, НЕ В IF RIGHT!)
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        game_over = True

    # self collision
    if head in snake:
        game_over = True

    # add head
    snake.insert(0, head)

    # food
    if head in food:
        score += 1
        food.remove(head)

        if len(food) == 0:
            food = generate_food(snake)
    else:
        snake.pop()

    # level
    new_level = score // 3 + 1
    if new_level > level:
        level = new_level
        speed += 1

    # draw
    screen.blit(image21, (0, 0))

    for segment in snake:
        pygame.draw.rect(screen, (50, 100, 255),
                         (segment[0], segment[1], BLOCK, BLOCK))

    for part in food:
        pygame.draw.rect(screen, RED,
                         (part[0], part[1], BLOCK, BLOCK))

    draw_text(f"Score: {score}", BLACK, 450, 10)
    draw_text(f"Level: {level}", BLACK, 250, 10)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()