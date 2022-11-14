
import pickle
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

clock = pygame.time.Clock()

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_width(), SCREEN.get_height()

pygame.display.set_caption("Zuckerburger")

startMenuScreen = StartMenu(SCREEN, clock)
screens = [startMenuScreen, TowerOfHanoi(SCREEN, clock), Klotski(SCREEN, clock), FindTheHiddenObj(SCREEN, clock), games.color_switch.MainGame(SCREEN, clock), None]


globals.initialize()

def send_data(time, puzzle_level):
    user = None
    with open('currentUser', 'rb') as f:
        user = pickle.load(f)

    dictToSend = {"hcid": str(user), 'time': str(time), 'puzzle_level': str(puzzle_level)}
    if res.status_code == 401:
        # Unauthorized
        pass
    res = requests.post(f'{baseUrl}/add-shit', json=dictToSend)

def main():
    start_time=0
    counting_minutes=0
    while True:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        startMenuScreen.start_button.changeColor(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if screens[globals.activeGameIndex] != None:
                    screens[globals.activeGameIndex].OnEvent(event)

                    # activeGameIndex += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    globals.activeGameIndex += 1
                    start_time = pygame.time.get_ticks()
                    print(start_time)
                if event.key == pygame.K_o:
                    globals.activeGameIndex += 1

                    print(start_time)
                #pass


        SCREEN.fill(BLACK)


        if screens[globals.activeGameIndex] != None:
            output = screens[globals.activeGameIndex].Update(dt)
            screens[globals.activeGameIndex].Render()

            if output != None:
                globals.activeGameIndex += 1

        if screens[globals.activeGameIndex] == None:
            SCREEN.fill((0,0,0))
            gameWonText = get_font(50).render("You Won", 1, (255, 255, 255))
            SCREEN.blit(gameOverText, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            send_data(counting_minutes, globals.activeGameIndex)



        if globals.activeGameIndex > 0:
            counting_time = pygame.time.get_ticks() - start_time

            # change milliseconds into minutes, seconds, milliseconds
            counting_minutes = str(counting_time//60000)
            counting_seconds = str( (counting_time%60000)//1000 )
            #counting_millisecond = str(counting_time%1000).zfill(3)
            timer_string = "%s:%s" % (counting_minutes, counting_seconds)

            text = get_font(50).render(str(timer_string), 1, (255,255,255))
            level_text = get_font(50).render(str(globals.activeGameIndex), 1, (255,255,255))
            SCREEN.blit(text, (10, 10))
            SCREEN.blit(level_text, (SCREEN_WIDTH//2, 10))

            if int(counting_minutes) > 60:
                SCREEN.fill((0,0,0))
                gameOverText = get_font(50).render("Game over, get lost", 1, (255, 255, 255))
                SCREEN.blit(gameOverText, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                send_data(counting_minutes, globals.activeGameIndex)

        pygame.display.flip()


if __name__ == "__main__":
    main()
