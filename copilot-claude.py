import pygame
import math
import sys
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Physics parameters
GRAVITY = 0.5
FRICTION = 0.99
BOUNCE_DAMPING = 0.8
ROTATION_SPEED = 0.02

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel_x = 0
        self.vel_y = 0
        
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Apply friction
        self.vel_x *= FRICTION
        self.vel_y *= FRICTION
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0
        self.vertices = []
        self.update_vertices()
    
    def update_vertices(self):
        self.vertices = []
        for i in range(6):
            angle = self.angle + (i * math.pi / 3)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.vertices.append((x, y))
    
    def rotate(self):
        self.angle += ROTATION_SPEED
        self.update_vertices()
    
    def draw(self, surface):
        pygame.draw.polygon(surface, BLUE, self.vertices, 2)

def check_collision(ball, hexagon):
    # Check collision with each edge of the hexagon
    for i in range(6):
        p1 = hexagon.vertices[i]
        p2 = hexagon.vertices[(i + 1) % 6]
        
        # Calculate normal vector of the wall
        wall_vector = (p2[0] - p1[0], p2[1] - p1[1])
        wall_length = math.sqrt(wall_vector[0]**2 + wall_vector[1]**2)
        normal = (-wall_vector[1]/wall_length, wall_vector[0]/wall_length)
        
        # Calculate distance from ball to line
        vec_to_ball = (ball.x - p1[0], ball.y - p1[1])
        distance = abs(vec_to_ball[0]*normal[0] + vec_to_ball[1]*normal[1])
        
        if distance < ball.radius:
            # Calculate reflection
            dot_product = ball.vel_x*normal[0] + ball.vel_y*normal[1]
            ball.vel_x = BOUNCE_DAMPING * (ball.vel_x - 2*dot_product*normal[0])
            ball.vel_y = BOUNCE_DAMPING * (ball.vel_y - 2*dot_product*normal[1])
            
            # Push ball out of the wall
            overlap = ball.radius - distance
            ball.x += overlap * normal[0]
            ball.y += overlap * normal[1]

def main():
    clock = pygame.time.Clock()
    
    # Create objects
    ball = Ball(WIDTH//2, HEIGHT//2, 15)
    hexagon = Hexagon(WIDTH//2, HEIGHT//2, 200)
    
    # Initial impulse to the ball
    ball.vel_x = 5
    ball.vel_y = -8
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Reset ball position and give it new random velocity on click
                ball.x = WIDTH//2
                ball.y = HEIGHT//2
                ball.vel_x = 5
                ball.vel_y = -8
        
        # Update
        hexagon.rotate()
        ball.update()
        check_collision(ball, hexagon)
        
        # Draw
        screen.fill(BLACK)
        hexagon.draw(screen)
        ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()