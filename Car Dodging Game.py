import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Dodging Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the car
car_width, car_height = 60, 100
car_x = width // 2 - car_width // 2
car_y = height - car_height - 10
car_speed = 5

# Set up the other cars
other_cars = []
other_car_width, other_car_height = 60, 100
other_car_speed = 3
num_other_cars = 5

# Set up the score
score = 0
font = pygame.font.Font(None, 36)

# Set up the background
lane_width = width // 3
line_height = 80
num_lines = height // line_height
line_y = -line_height

# Game over flag
game_over = False

# Generate initial other cars
for _ in range(num_other_cars):
    other_car_x = random.randint(0, width - other_car_width)
    other_car_y = random.randint(-height, -other_car_height)
    other_cars.append((other_car_x, other_car_y))

# Game loop
while not game_over:
    display.fill(BLACK)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                score = 0
                game_over = False
                car_x = width // 2 - car_width // 2
                car_y = height - car_height - 10
                other_cars = []
                for _ in range(num_other_cars):
                    other_car_x = random.randint(0, width - other_car_width)
                    other_car_y = random.randint(-height, -other_car_height)
                    other_cars.append((other_car_x, other_car_y))
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Handle car movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < width - car_width:
            car_x += car_speed

        # Update other car positions
        for i in range(len(other_cars)):
            other_cars[i] = (other_cars[i][0], other_cars[i][1] + other_car_speed)
            if other_cars[i][1] > height:
                other_car_x = random.randint(0, width - other_car_width)
                other_car_y = random.randint(-height, -other_car_height)
                other_cars[i] = (other_car_x, other_car_y)
                score += 1

            # Check for collision with other car
            if car_y < other_cars[i][1] + other_car_height and car_y + car_height > other_cars[i][1]:
                if car_x < other_cars[i][0] + other_car_width and car_x + car_width > other_cars[i][0]:
                    game_over = True

        # Draw the background
        for i in range(num_lines):
            pygame.draw.rect(display, GREY, (width // 2 - 5, line_y + i * line_height, 10, 40))

        # Draw the car
        pygame.draw.rect(display, RED, (car_x, car_y, car_width, car_height))

        # Draw the other cars
        for other_car in other_cars:
            pygame.draw.rect(display, WHITE, (other_car[0], other_car[1], other_car_width, other_car_height))

        # Display the score
        score_text = font.render("Score: " + str(score), True, WHITE)
        display.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(60)

    # Game over menu
    while game_over:
        display.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render("Score: " + str(score), True, WHITE)
        restart_text = font.render("Press R to Restart or ESC to Quit", True, WHITE)
        display.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
        display.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
        display.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))
        pygame.display.update()

# Quit Pygame
pygame.quit()
