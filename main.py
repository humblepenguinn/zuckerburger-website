import pickle
from games.tetris import Tetris
import globals
import pygame
import requests

from utils import *
from settings import *
from globals import *
from debug import *

from games.tower_of_hanoi import *
from games.find_the_hidden_object import *
from games.klotski import *
import games.color_switch
from start_menu import StartMenu

from datetime import datetime

clock = pygame.time.Clock()

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_width(), SCREEN.get_height()

pygame.display.set_caption("Zuckerburger")

startMenuScreen = StartMenu(SCREEN, clock)
screens = [startMenuScreen, Tetris(SCREEN, clock), TowerOfHanoi(SCREEN, clock), Klotski(SCREEN, clock), FindTheHiddenObj(SCREEN, clock), games.color_switch.MainGame(SCREEN, clock)]

globals.initialize()

defaultFont = get_font(50)

def send_data(time, puzzle_level):
    user = None
    with open('currentUser', 'rb') as f:
        user = pickle.load(f)

    dictToSend = {"hcid": str(user), 'time': str(time), 'puzzle_level': str(puzzle_level)}
    res = requests.post(f'{base_url}/add-shit', json=dictToSend)
    if res.status_code == 401:
        # Unauthorized
        pass


def main():
    start_time = datetime.now()
    won = False
    completed = False

    while True:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        startMenuScreen.start_button.changeColor(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if globals.activeGameIndex < len(screens) and screens[globals.activeGameIndex] != None:
                screens[globals.activeGameIndex].OnEvent(event)

                # activeGameIndex += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    globals.activeGameIndex += 1
                    start_time = datetime.now()
                    print(start_time)
                if event.key == pygame.K_o:
                    globals.activeGameIndex += 1

                    if globals.activeGameIndex >= len(screens):
                        # Completed all the games
                        won = True
                        completed = True

                    print(start_time)
                #pass


        SCREEN.fill(BLACK)

        if not completed and globals.activeGameIndex < len(screens) and screens[globals.activeGameIndex] != None:
            output = screens[globals.activeGameIndex].Update(dt)
            screens[globals.activeGameIndex].Render()

            if globals.activeGameIndex != 0:
                time_taken = datetime.now() - start_time

                text = get_font(50).render(str(time_taken)[2:7], 1, (255,255,255))
                level_text = get_font(50).render(str(globals.activeGameIndex), 1, (255,255,255))
                SCREEN.blit(text, (10, 10))
                SCREEN.blit(level_text, (SCREEN_WIDTH//2, 10))

                if int(time_taken.total_seconds()) >= 60 * 60:
                    completed = True
                    send_data(time_taken.total_seconds() // 60, globals.activeGameIndex)

            if output != None and output is True:
                globals.activeGameIndex += 1

                if globals.activeGameIndex >= len(screens):
                    # Completed all the games
                    send_data(time_taken.total_seconds() // 60, globals.activeGameIndex)
                    won = True
                    completed = True

        if won:
            SCREEN.fill((0,0,0))
            gameWonText = get_font(50).render("You Won", True, (255, 255, 255))
            SCREEN.blit(gameWonText, gameWonText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))

        elif completed:
            SCREEN.fill((0,0,0))
            gameOverText = get_font(50).render("Game over, get lost", 1, (255, 255, 255))
            SCREEN.blit(gameOverText, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        pygame.display.update()


if __name__ == "__main__":
    main()
