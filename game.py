"""
Chrome Dino Game - Refactored with Classes and Improvements
A pygame implementation of the Chrome browser's offline game
"""

import pygame
import random
import sys
from typing import Tuple

# Initialize Pygame
pygame.init()

# =========================================================
# CONSTANTS - Screen Configuration
# =========================================================
WIDTH, HEIGHT = 800, 400
BACKGROUND_COLOR = (247, 247, 247)  # Off-White (Chrome style)
BLACK = (83, 83, 83)  # Dark Gray (Retro)
FPS = 60

# =========================================================
# CONSTANTS - Game Physics
# =========================================================
GRAVITY = 0.8
DINO_JUMP_VELOCITY = -14
INITIAL_OBSTACLE_SPEED = 7
OBSTACLE_SPEED_INCREMENT = 0.2

# =========================================================
# CONSTANTS - Dino Properties
# =========================================================
DINO_X = 50
DINO_Y = 300
DINO_WIDTH = 40
DINO_HEIGHT = 50

# =========================================================
# CONSTANTS - Obstacle (Cactus) Properties
# =========================================================
CACTUS_Y = 300
CACTUS_WIDTH = 30
CACTUS_HEIGHT = 50

# =========================================================
# CONSTANTS - Ground Properties
# =========================================================
GROUND_Y = 340
GROUND_WIDTH = 1200
GROUND_HEIGHT = 20

# =========================================================
# CONSTANTS - Cloud Properties
# =========================================================
CLOUD_WIDTH = 60
CLOUD_HEIGHT = 25
CLOUD_SPEED = 1.5
INITIAL_CLOUDS = [
    [600, 100],
    [900, 80]
]

# =========================================================
# IMAGE LOADING WITH ERROR HANDLING
# =========================================================
def load_image(filename: str, width: int, height: int) -> pygame.Surface:
    """Load and scale an image with error handling."""
    try:
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, (width, height))
    except pygame.error as e:
        print(f"Error loading {filename}: {e}")
        print("Please ensure all image files are in the same directory as this script.")
        pygame.quit()
        sys.exit()

# Load images
img_dino = load_image("dino.png", DINO_WIDTH, DINO_HEIGHT)
img_cactus = load_image("cactus.png", CACTUS_WIDTH, CACTUS_HEIGHT)
img_cloud = load_image("cloud.png", CLOUD_WIDTH, CLOUD_HEIGHT)
img_ground = load_image("ground.png", GROUND_WIDTH, GROUND_HEIGHT)

# =========================================================
# DINO CLASS
# =========================================================
class Dino:
    """Represents the dinosaur player character."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.is_jumping = False
    
    def jump(self) -> None:
        """Make the dino jump."""
        if not self.is_jumping:
            self.vel_y = DINO_JUMP_VELOCITY
            self.is_jumping = True
    
    def update(self) -> None:
        """Update dino physics (gravity and collision with ground)."""
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Keep dino on ground
        if self.y >= DINO_Y:
            self.y = DINO_Y
            self.is_jumping = False
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle for the dino."""
        return pygame.Rect(self.x, self.y, DINO_WIDTH, DINO_HEIGHT)
    
    def reset(self) -> None:
        """Reset dino to starting position."""
        self.x = DINO_X
        self.y = DINO_Y
        self.vel_y = 0
        self.is_jumping = False

# =========================================================
# OBSTACLE CLASS
# =========================================================
class Obstacle:
    """Represents a cactus obstacle."""
    
    def __init__(self, x: int, speed: float):
        self.x = x
        self.speed = speed
    
    def update(self) -> None:
        """Move obstacle to the left."""
        self.x -= self.speed
    
    def is_off_screen(self) -> bool:
        """Check if obstacle has left the screen."""
        return self.x < -CACTUS_WIDTH
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle for the cactus."""
        return pygame.Rect(self.x, CACTUS_Y, CACTUS_WIDTH, CACTUS_HEIGHT)
    
    def reset(self, speed: float) -> None:
        """Reset obstacle to the right side of screen."""
        self.x = WIDTH
        self.speed = speed

# =========================================================
# GROUND CLASS
# =========================================================
class Ground:
    """Represents the scrolling ground."""
    
    def __init__(self):
        self.x1 = 0
        self.x2 = GROUND_WIDTH
        self.y = GROUND_Y
    
    def update(self, speed: float) -> None:
        """Scroll the ground."""
        self.x1 -= speed
        self.x2 -= speed
        
        # Wrap around when off-screen
        if self.x1 <= -GROUND_WIDTH:
            self.x1 = self.x2 + GROUND_WIDTH
        if self.x2 <= -GROUND_WIDTH:
            self.x2 = self.x1 + GROUND_WIDTH
    
    def reset(self) -> None:
        """Reset ground to starting position."""
        self.x1 = 0
        self.x2 = GROUND_WIDTH

# =========================================================
# CLOUD CLASS
# =========================================================
class Cloud:
    """Represents a cloud in the background."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def update(self) -> None:
        """Move cloud slowly to the left."""
        self.x -= CLOUD_SPEED
        
        # Reset when off-screen
        if self.x < -CLOUD_WIDTH:
            self.x = WIDTH + random.randint(50, 200)
            self.y = random.randint(50, 120)
    
    def get_position(self) -> Tuple[int, int]:
        """Get cloud position."""
        return (self.x, self.y)

# =========================================================
# GAME CLASS
# =========================================================
class Game:
    """Main game controller."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chrome Dino Game - Pixel Background")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20, bold=True)
        
        # Game state
        self.dino = Dino(DINO_X, DINO_Y)
        self.obstacle = Obstacle(WIDTH, INITIAL_OBSTACLE_SPEED)
        self.ground = Ground()
        self.clouds = [Cloud(x, y) for x, y in INITIAL_CLOUDS]
        
        self.score = 0
        self.game_over = False
        self.running = True
    
    def reset_game(self) -> None:
        """Reset all game variables."""
        self.dino.reset()
        self.obstacle.reset(INITIAL_OBSTACLE_SPEED)
        self.ground.reset()
        self.score = 0
        self.game_over = False
    
    def handle_events(self) -> None:
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.dino.jump()
    
    def update(self) -> None:
        """Update game logic."""
        if self.game_over:
            return
        
        # Update dino physics
        self.dino.update()
        
        # Update ground
        self.ground.update(self.obstacle.speed)
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update()
        
        # Update obstacle
        self.obstacle.update()
        if self.obstacle.is_off_screen():
            self.obstacle.reset(self.obstacle.speed)
            self.score += 1
            self.obstacle.speed += OBSTACLE_SPEED_INCREMENT
        
        # Check collision
        if self.dino.get_rect().colliderect(self.obstacle.get_rect()):
            self.game_over = True
    
    def draw(self) -> None:
        """Draw all game elements."""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw clouds
        for cloud in self.clouds:
            self.screen.blit(img_cloud, cloud.get_position())
        
        # Draw ground
        self.screen.blit(img_ground, (self.ground.x1, self.ground.y))
        self.screen.blit(img_ground, (self.ground.x2, self.ground.y))
        
        # Draw dino and cactus
        self.screen.blit(img_dino, (self.dino.x, self.dino.y))
        self.screen.blit(img_cactus, (self.obstacle.x, CACTUS_Y))
        
        # Draw score
        score_text = self.font.render(f"HI {self.score:05d}", True, BLACK)
        self.screen.blit(score_text, (self.width - 150, 20))
        
        # Draw game over message
        if self.game_over:
            go_text = self.font.render("G A M E   O V E R", True, BLACK)
            self.screen.blit(go_text, (self.width // 2 - 110, self.height // 2 - 20))
            restart_text = self.font.render("Press SPACE to restart", True, BLACK)
            self.screen.blit(restart_text, (self.width // 2 - 130, self.height // 2 + 20))
        
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.run()
