import pygame
from pygame.math import Vector3
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Car Soccer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define color schemes
color_schemes = {
    "Default": {
        "BACKGROUND": BLACK,
        "PLAYER_COLOR": BLUE,
        "OPPONENT_COLOR": RED,
        "BALL_COLOR": WHITE,
        "GOAL_COLOR": GREEN,
        "TEXT_COLOR": WHITE
    },
    "Ocean Breeze": {
        "BACKGROUND": (0, 128, 128),
        "PLAYER_COLOR": (0, 255, 255),
        "OPPONENT_COLOR": (255, 128, 0),
        "BALL_COLOR": (255, 255, 255),
        "GOAL_COLOR": (0, 255, 128),
        "TEXT_COLOR": (255, 255, 255)
    },
    "Night Mode": {
        "BACKGROUND": (0, 0, 0),
        "PLAYER_COLOR": (255, 255, 255),
        "OPPONENT_COLOR": (128, 128, 128),
        "BALL_COLOR": (255, 0, 0),
        "GOAL_COLOR": (0, 0, 255),
        "TEXT_COLOR": (255, 255, 255)
    }
}

# Set default color scheme
current_scheme = color_schemes["Default"]

# Car class
class Car:
    def __init__(self, x, y, color):
        self.pos = Vector3(x, y, 0)
        self.vel = Vector3(0, 0, 0)
        self.color = color
        self.size = 20

    def update(self):
        self.pos += self.vel
        self.vel *= 0.9  # increased friction to reduce glide
        
        # Boundary checking
        self.pos.x = max(0, min(width - self.size, self.pos.x))
        self.pos.y = max(0, min(height - self.size, self.pos.y))

    def draw(self):
        pygame.draw.rect(display, self.color, (int(self.pos.x), int(self.pos.y), self.size, self.size))

# Ball class
class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = Vector3(width // 2, height // 2, 0)
        self.vel = Vector3(random.choice([-2, 2]), random.choice([-2, 2]), 0)
        self.radius = 10

    def update(self):
        self.pos += self.vel
        self.vel *= 0.99  # friction

        # Boundary checking
        if self.pos.x < self.radius or self.pos.x > width - self.radius:
            self.vel.x *= -1
        if self.pos.y < self.radius or self.pos.y > height - self.radius:
            self.vel.y *= -1

    def draw(self):
        pygame.draw.circle(display, current_scheme["BALL_COLOR"], (int(self.pos.x), int(self.pos.y)), self.radius)

# Create game objects
player = Car(100, height // 2, current_scheme["PLAYER_COLOR"])
opponent = Car(width - 120, height // 2, current_scheme["OPPONENT_COLOR"])
ball = Ball()

# Scoring
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Main game loop
running = True
clock = pygame.time.Clock()

def color_selection():
    global current_scheme, player, opponent
    color_options = list(color_schemes.keys())
    selected = 0  # Default to the first color scheme
    
    while True:
        display.fill(current_scheme["BACKGROUND"])
        
        title = font.render('Select Color Scheme', True, current_scheme["TEXT_COLOR"])
        title_rect = title.get_rect(center=(width//2, height//4))
        display.blit(title, title_rect)
        
        for i, scheme in enumerate(color_options):
            color = current_scheme["PLAYER_COLOR"] if i == selected else current_scheme["TEXT_COLOR"]
            option = font.render(scheme, True, color)
            option_rect = option.get_rect(center=(width//2, height//2 + i * 50))
            display.blit(option, option_rect)
            
            # Draw color preview for the selected scheme
            if i == selected:
                preview_rect = pygame.Rect(width//2 + 150, height//2 - 100, 200, 50)
                pygame.draw.rect(display, color_schemes[scheme]["BACKGROUND"], preview_rect)
                pygame.draw.rect(display, color_schemes[scheme]["PLAYER_COLOR"], [preview_rect.x + 10, preview_rect.y + 10, 30, 30])
                pygame.draw.rect(display, color_schemes[scheme]["OPPONENT_COLOR"], [preview_rect.x + 60, preview_rect.y + 10, 30, 30])
                pygame.draw.rect(display, color_schemes[scheme]["BALL_COLOR"], [preview_rect.x + 110, preview_rect.y + 10, 30, 30])
                pygame.draw.rect(display, color_schemes[scheme]["GOAL_COLOR"], [preview_rect.x + 160, preview_rect.y + 10, 30, 30])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(color_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(color_options)
                elif event.key == pygame.K_RETURN:
                    current_scheme = color_schemes[color_options[selected]]
                    player.color = current_scheme["PLAYER_COLOR"]
                    opponent.color = current_scheme["OPPONENT_COLOR"]
                    return

def difficulty_selection():
    difficulties = ["Easy", "Medium", "Hard"]
    speeds = [0.2, 0.3, 0.4]
    selected = 1  # Default to Medium
    
    while True:
        display.fill(current_scheme["BACKGROUND"])
        
        title = font.render('Select Difficulty', True, current_scheme["TEXT_COLOR"])
        title_rect = title.get_rect(center=(width//2, height//4))
        display.blit(title, title_rect)
        
        for i, difficulty in enumerate(difficulties):
            color = current_scheme["PLAYER_COLOR"] if i == selected else current_scheme["TEXT_COLOR"]
            option = font.render(difficulty, True, color)
            option_rect = option.get_rect(center=(width//2, height//2 + i * 50))
            display.blit(option, option_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    return speeds[selected]

color_selection()
opponent_speed = difficulty_selection()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.vel.y -= 0.3  # reduced speed
    if keys[pygame.K_s]:
        player.vel.y += 0.3  # reduced speed
    if keys[pygame.K_a]:
        player.vel.x -= 0.3  # reduced speed
    if keys[pygame.K_d]:
        player.vel.x += 0.3  # reduced speed

    # Simple AI for opponent
    if opponent.pos.y < ball.pos.y:
        opponent.vel.y += opponent_speed
    else:
        opponent.vel.y -= opponent_speed
    if opponent.pos.x < ball.pos.x:
        opponent.vel.x += opponent_speed
    else:
        opponent.vel.x -= opponent_speed

    # Update game objects
    player.update()
    opponent.update()
    ball.update()

    # Improved collision detection
    for car in [player, opponent]:
        if (abs(car.pos.x - ball.pos.x) < (car.size + ball.radius) and
            abs(car.pos.y - ball.pos.y) < (car.size + ball.radius)):
            normal = (ball.pos - car.pos).normalize()
            ball.vel = normal * (ball.vel.length() + car.vel.length() * 0.5)

    # Check for goals
    if ball.pos.x < 0 and height // 2 - 50 < ball.pos.y < height // 2 + 50:
        opponent_score += 1
        ball.reset()
    elif ball.pos.x > width and height // 2 - 50 < ball.pos.y < height // 2 + 50:
        player_score += 1
        ball.reset()

    # Draw everything
    display.fill(current_scheme["BACKGROUND"])
    player.draw()
    opponent.draw()
    ball.draw()

    # Draw goals
    pygame.draw.rect(display, current_scheme["GOAL_COLOR"], (0, height // 2 - 50, 10, 100))
    pygame.draw.rect(display, current_scheme["GOAL_COLOR"], (width - 10, height // 2 - 50, 10, 100))

    # Display score
    score_text = font.render(f"{player_score} - {opponent_score}", True, current_scheme["TEXT_COLOR"])
    display.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
