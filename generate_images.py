"""
Image Generator for Chrome Dino Game
Automatically creates all required PNG images using pygame
"""

import pygame
import sys

def create_dino_image(filename: str = "dino.png", width: int = 40, height: int = 50):
    """Create a simple dinosaur sprite."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Body
    pygame.draw.rect(surface, (83, 83, 83), (5, 20, 20, 20))
    # Head
    pygame.draw.circle(surface, (83, 83, 83), (28, 18), 8)
    # Eye
    pygame.draw.circle(surface, (255, 255, 255), (30, 16), 3)
    pygame.draw.circle(surface, (0, 0, 0), (31, 16), 1)
    # Legs
    pygame.draw.line(surface, (83, 83, 83), (8, 40), (8, 48), 3)
    pygame.draw.line(surface, (83, 83, 83), (18, 40), (18, 48), 3)
    # Tail
    pygame.draw.line(surface, (83, 83, 83), (5, 25), (0, 20), 3)
    
    pygame.image.save(surface, filename)
    print(f"✓ Created {filename}")

def create_cactus_image(filename: str = "cactus.png", width: int = 30, height: int = 50):
    """Create a simple cactus sprite."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main stem
    pygame.draw.rect(surface, (100, 150, 50), (10, 10, 10, 40))
    # Left arm
    pygame.draw.line(surface, (100, 150, 50), (10, 20), (2, 20), 4)
    # Right arm
    pygame.draw.line(surface, (100, 150, 50), (20, 30), (28, 30), 4)
    # Spikes
    for y in range(15, 50, 8):
        pygame.draw.circle(surface, (100, 150, 50), (9, y), 2)
        pygame.draw.circle(surface, (100, 150, 50), (21, y), 2)
    
    pygame.image.save(surface, filename)
    print(f"✓ Created {filename}")

def create_cloud_image(filename: str = "cloud.png", width: int = 60, height: int = 25):
    """Create a simple cloud sprite."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Cloud circles
    pygame.draw.circle(surface, (200, 200, 200), (10, 15), 8)
    pygame.draw.circle(surface, (200, 200, 200), (20, 10), 10)
    pygame.draw.circle(surface, (200, 200, 200), (35, 8), 10)
    pygame.draw.circle(surface, (200, 200, 200), (50, 12), 9)
    pygame.draw.circle(surface, (200, 200, 200), (55, 18), 8)
    
    pygame.image.save(surface, filename)
    print(f"✓ Created {filename}")

def create_ground_image(filename: str = "ground.png", width: int = 1200, height: int = 20):
    """Create a simple ground sprite."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main ground bar
    pygame.draw.rect(surface, (83, 83, 83), (0, 0, width, 2))
    
    # Repeating ground pattern
    for x in range(0, width, 20):
        pygame.draw.line(surface, (200, 200, 200), (x, 5), (x + 10, 15), 1)
        pygame.draw.line(surface, (200, 200, 200), (x + 10, 15), (x + 20, 5), 1)
    
    pygame.image.save(surface, filename)
    print(f"✓ Created {filename}")

def main():
    """Generate all game images."""
    print("=" * 50)
    print("Chrome Dino Game - Image Generator")
    print("=" * 50)
    print()
    
    # Initialize pygame for image creation
    pygame.init()
    
    try:
        create_dino_image()
        create_cactus_image()
        create_cloud_image()
        create_ground_image()
        
        print()
        print("=" * 50)
        print("✓ All images created successfully!")
        print("=" * 50)
        print()
        print("You can now run: python game.py")
        print()
        
    except Exception as e:
        print(f"✗ Error creating images: {e}")
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
