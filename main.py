
import pygame
import requests
import pickle

from utils import *
from settings import *
from globals import *

from games.tower_of_hanoi import *
from games.find_the_hidden_object import *
from games.klotski import *
import games.color_switch
from start_menu import StartMenu

clock = pygame.time.Clock()

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_width(), SCREEN.get_height()

pygame.display.set_caption("Zuckerburger")

startMenuScreen = StartMenu(SCREEN, clock)
screens = [Klotski(SCREEN, clock), startMenuScreen, TowerOfHanoi(SCREEN, clock), FindTheHiddenObj(SCREEN, clock), games.color_switch.MainGame(SCREEN), None]

activeGameIndex = 0


def main():
    global activeGameIndex

    while True:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        startMenuScreen.start_button.changeColor(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if screens[activeGameIndex] != None:
                screens[activeGameIndex].OnEvent(event)

                    # activeGameIndex += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    activeGameIndex += 1
                #pass


        SCREEN.fill(BLACK)

        if screens[activeGameIndex] != None:
            gameOver = screens[activeGameIndex].Update(dt)
            screens[activeGameIndex].Render()

        if screens[activeGameIndex] == None:
            requests.post(f'{baseUrl}/logout')

        pygame.display.flip()

if __name__ == "__main__":
    main()
