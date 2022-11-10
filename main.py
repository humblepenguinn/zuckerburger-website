
import pygame

from utils import *
from settings import *

from tower_of_hanoi import TowerOfHanoi
from start_menu import StartMenu
from game import Game

clock = pygame.time.Clock()

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_width(), SCREEN.get_height()

pygame.display.set_caption("Zuckerburger")

games = []
games.append(StartMenu(SCREEN, clock))
games.append(TowerOfHanoi(SCREEN, clock))

activeGameIndex = 0

def main():
    global activeGameIndex

    while True:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    activeGameIndex += 1

            if games[activeGameIndex] != None:
                games[activeGameIndex].OnEvent(event)

        SCREEN.fill(BLACK)

        if games[activeGameIndex] != None:
            gameOver = games[activeGameIndex].Update(dt)
            games[activeGameIndex].Render()

        pygame.display.update()

if __name__ == "__main__":
    main()