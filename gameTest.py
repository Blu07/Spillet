import pygame
import os
import numpy as np

# Define PID controller parameters
kp = 0.1
ki = 0.1
kd = 0.1

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Use super() for cleaner inheritance
        self.image = pygame.Surface((40, 40))  # Placeholder image
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect(center=(200, 200))  # Set the initial position

        self.speed = np.zeros(2)  # Initial speed vector
        self.targetPlayerPos = np.array([200, 200])  # Initialize target position

        # Initialize PID controller variables
        self.prev_error = np.zeros(2)
        self.integral = np.zeros(2)

    def update(self, dt):
        """
        Update the position based on speed vector, target position, and PID control.
        """

        # Update player position based on speed vector
        self.rect.x += int(self.speed[0] * dt)
        self.rect.y += int(self.speed[1] * dt)

        # PID control towards target position
        error = self.targetPlayerPos - np.array([self.rect.x, self.rect.y])
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = kp * error + ki * self.integral + kd * derivative
        self.prev_error = error

        # Adjust speed vector based on PID control output
        self.speed = output

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Create player sprite
player = PlayerSprite()
all_sprites = pygame.sprite.Group(player)

running = True
while running:
    dt = clock.tick(60) / 1000  # Time in seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # When left mouse button is pressed, update target position
                player.targetPlayerPos = pygame.mouse.get_pos()

    all_sprites.update(dt)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
