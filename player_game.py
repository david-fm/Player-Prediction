import pygame
from math import sqrt
from queue import PriorityQueue
# TODO ERROR: KeyError: (190, 190)
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the width and height of the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
ENEMY_PATH_REFRESH_RATE = 60 # The enemy will recalculate its path every 120 frames
ENEMY_SPEED = 3 # The enemy will move 5 pixels every frame

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
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

class Enemy(pygame.sprite.Sprite):
    """ A class to represent the enemy object """
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.player = player
        self.counter = ENEMY_PATH_REFRESH_RATE-1 # Used to slow down the enemy

        self.path = None # The path the enemy will follow, it will be recalculated every 120 frames

    def update(self):
        """ Move the enemy object """
        self.counter += 1 # Slow down the enemy
        if self.counter % ENEMY_PATH_REFRESH_RATE == 0:
            path = self.a_star(self.rect.topleft, self.player.rect.topleft)
            path = self.reconstruct_path(path[0], self.rect.topleft, self.player.rect.topleft)
            self.path = path[:-1]
            self.counter = 0
        if self.path:
            next_tile = self.path.pop()
            dx = next_tile[0] - self.rect.x
            dy = next_tile[1] - self.rect.y
            self.rect.x += dx
            self.rect.y += dy
    
    def heuristic(self, a, b) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    def neighbors(self, node):
        (x, y) = node
        neighbors = [(x + ENEMY_SPEED, y), (x - ENEMY_SPEED, y), (x, y + ENEMY_SPEED), (x, y - ENEMY_SPEED)]
        # Remove neighbors that are outside the screen
        neighbors = filter(lambda x: x[0] >= 0 and x[0] < SCREEN_WIDTH, neighbors)
        neighbors = filter(lambda x: x[1] >= 0 and x[1] < SCREEN_HEIGHT, neighbors)
        return neighbors
    
    def cost(self, a, b):
        return 1

    def a_star(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        return came_from, cost_so_far
    
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        return path

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption("RL Playground")

# Create the player object
player = Player()
enemy = Enemy(player)

# Create a group to hold the player object
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

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

    if pygame.sprite.collide_rect(player, enemy):
        print("Game Over!")
        done = True
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
