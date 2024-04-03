from keyboard import *
import random as rnd
import time
import math
import pygame
import os
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Scene:
    def __init__(self, surface):
        self.gameboard = surface
        self.interrupted = False
        self.playerSprite = PlayerSprite()
       

    def render(self):
        if not self.interrupted:
            self.playerSprite.update(self.gameboard)  # Call update method directly
            # Draw the player sprite on the gameboard
            self.playerSprite.draw(self.gameboard)


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Use super() for cleaner inheritance
        self.image = pygame.image.load(os.path.join("sprites", "player1.png"))
        self.rect = self.image.get_rect(center=playerPos)  # Set the initial position

        # Initialize speed vectors and vectors affecting speed
        self.speedVector = np.zeros(2)
        self.weight = 10
        self.moveResistance = 10.3
        # Initialize PID controller variables
        self.prev_error = np.zeros(2)
        self.integral = np.zeros(2)


    def update(self, surface):
        """
        Update the position based on speed vector
        """
        if pygame.mouse.get_pressed()[0]:
            self.updateSpeedVectorPID(surface)
        else:
            if hasattr(self, 'threadInitialLength'):
                delattr(self, 'threadInitialLength')

        self.speedVector *=  self.weight/self.moveResistance

        # Update player position based on speed vector
        self.rect.x += self.speedVector[0]
        self.rect.y += self.speedVector[1]


        


        # # Get Boolean value for which keys are pressed for movement
        # keys = pygame.key.get_pressed()
        # up = keys[pygame.K_w] or keys[pygame.K_i] or keys[pygame.K_UP] or keys[pygame.K_KP_8]
        # down = keys[pygame.K_s] or keys[pygame.K_k] or keys[pygame.K_DOWN] or keys[pygame.K_KP_5] or keys[pygame.K_KP_2]
        # left = keys[pygame.K_a] or keys[pygame.K_j] or keys[pygame.K_LEFT] or keys[pygame.K_KP_4]
        # right = keys[pygame.K_d] or keys[pygame.K_l] or keys[pygame.K_RIGHT] or keys[pygame.K_KP_6]

        # # Change values based directly on keys pressed. Pro: Opposites cancel out.
        # if up:
        #     change_y -= 1
        # if down:
        #     change_y += 1
        # if right:
        #     change_x += 1
        # if left:
        #     change_x -= 1
        
        # # Account for vertical movement
        # # Player moves diagonally if both horizontal and vertical vectors have values.
        # if change_x and change_y:
        #     change_x /= math.sqrt(2)
        #     change_y /= math.sqrt(2)

        # # Apply changes
        # self.rect.x += speed * change_x * dt
        # self.rect.y += speed * change_y * dt

    def updateSpeedVectorPID(self, surface):
        
        global dt
        tension = 1.1
        Kp = 0.001
        Ki = 0.01
        Kd = 0.01



        mousePos = pygame.mouse.get_pos()
        playerPos = (self.rect.x, self.rect.y)

        mouseVec = np.array(mousePos)
        playerVec = np.array(playerPos)

        threadVec = playerVec - mouseVec
        threadLen = np.linalg.norm(threadVec)


        if not hasattr(self, 'threadInitialLength'):
            self.threadInitialLength = np.linalg.norm(threadVec)

        directionVec = threadVec / threadLen
        self.targetPlayerPos = mouseVec + (directionVec * self.threadInitialLength)
        
        self.drawThread(surface, mousePos, playerPos, int(threadLen/self.threadInitialLength))

        if not threadLen < self.threadInitialLength:
            # Move towards the target point with PID control
            error = np.array(self.targetPlayerPos) - playerVec
            self.integral += error
            derivative = (error - self.prev_error) / dt
            output = Kp * error + Ki * self.integral + Kd * derivative
            self.prev_error = error

            self.speedVector = output
        
    
            

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Blit the sprite onto the surface
        

    def drawThread(self, surface, start, end, stretch):
        pygame.draw.line(surface, (255, 0, 0), start, end, stretch*3)


scene = Scene(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#4b7382")

    scene.render()
   

    screen.blit(scene.gameboard, (0, 0))

    # Flip the display
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()


'''from keyboard import *
import random as rnd, time, math, pygame, os


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)



class Scene:
    def __init__(self, surface):
        self.gameboard = surface
        self.interrupted = False
        
        self.playerSprite = PlayerSprite()
        

    def render(self):
        if not self.interrupted:
            pygame.sprite.GroupSingle.update(self.playerSprite)

        pygame.sprite.GroupSingle.draw(self.playerSprite, self.gameboard)



class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the player, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.image.load(os.path.join("sprites", "player1.png"))

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

pygame.sprite.Group.draw

scene = Scene(screen)

group = pygame.sprite.Group()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#4b7382")

    # pygame.draw.circle(screen, "#9c0317", playerPos, 40)

    scene.render()

    screen.blit(scene.gameboard, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerPos.y -= 300 * dt
    if keys[pygame.K_s]:
        playerPos.y += 300 * dt
    if keys[pygame.K_a]:
        playerPos.x -= 300 * dt
    if keys[pygame.K_d]:
        playerPos.x += 300 * dt


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()
'''
