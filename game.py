from keyboard import *
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
            self.playerSprite.update()  # Call update method directly
            self.playerSprite.draw(self.gameboard)  # Draw the player sprite on the gameboard


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Use super() for cleaner inheritance
        self.image = pygame.image.load(os.path.join("sprites", "player1.png"))
        self.rect = self.image.get_rect(center=playerPos)  # Set the initial position

    def update(self):
        # Update the position based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 300 * dt
        if keys[pygame.K_s]:
            self.rect.y += 300 * dt
        if keys[pygame.K_a]:
            self.rect.x -= 300 * dt
        if keys[pygame.K_d]:
            self.rect.x += 300 * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Blit the sprite onto the surface

class Boundary:
    def __init__(self) -> None:
        self.rect = pygame.rect(20, 30)



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

