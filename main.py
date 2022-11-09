
import pygame

from utils import *
from settings import *

from tower_of_hanoi import TowerOfHanoi

clock = pygame.time.Clock()

pygame.init()

towerOfHanoi = TowerOfHanoi(SCREEN)

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_width(), SCREEN.get_height()

pygame.display.set_caption("Zuckerburger")

def main():
    while True:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            towerOfHanoi.OnEvent(event)

        SCREEN.fill(BLACK)

        towerOfHanoi.Update()
        towerOfHanoi.Render()

        pygame.display.update()

if __name__ == "__main__":
    main()