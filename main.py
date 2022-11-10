
import pygame

from utils import *
from settings import *

from tower_of_hanoi import TowerOfHanoi
from game import Game

clock = pygame.time.Clock()

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_width(), SCREEN.get_height()

pygame.display.set_caption("Zuckerburger")

games = []
games.append(TowerOfHanoi(SCREEN, clock))

activeGameIndex = 0

def main():
    while True:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if games[activeGameIndex] != None:
                games[activeGameIndex].OnEvent(event)

        SCREEN.fill(BLACK)

        if games[activeGameIndex] != None:
            obj = games[activeGameIndex].Update()
            games[activeGameIndex].Render()

            print(obj)

        pygame.display.update()

if __name__ == "__main__":
    main()