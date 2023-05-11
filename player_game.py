import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

class Player(pygame.sprite.Sprite):
    """ A class to represent the player object """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT // 2 - self.rect.height // 2

    def update(self):
        """ Move the player object """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption("RL Playground")

# Create the player object
player = Player()

# Create a group to hold the player object
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set the game loop flag
done = False

# Create a clock to manage the frame rate
clock = pygame.time.Clock()

# Game loop
while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update the player object
    all_sprites.update()

    # Fill the screen with black color
    screen.fill(BLACK)

    # Draw all sprites on the screen
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
