
import globals
import pygame
import requests
import pickle

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

def main():
    start_time=0
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


            if output is not None:
                if globals.activeGameIndex == 1: # tower of hanoi
                    globals.score += (10 - (output - 7))
                    print(globals.score)
                    globals.activeGameIndex += 1

                if globals.activeGameIndex == 4: # color switch we directly add the score no need for no of moves
                    globals.activeGameIndex += 1
                    globals.score += output


            screens[globals.activeGameIndex].Render()

        if screens[globals.activeGameIndex] == None:
            requests.post(f'{baseUrl}/logout')


        if globals.activeGameIndex > 0:
            counting_time = pygame.time.get_ticks() - start_time

            # change milliseconds into minutes, seconds, milliseconds
            counting_minutes = str(counting_time//60000)
            counting_seconds = str( (counting_time%60000)//1000 )
            #counting_millisecond = str(counting_time%1000).zfill(3)

            timer_string = "%s:%s" % (counting_minutes, counting_seconds)

            text = get_font(50).render(str(timer_string), 1, (255,255,255))
            score_text = get_font(50).render(str(globals.score), 1, (255,255,255))
            level_text = get_font(50).render(str(globals.activeGameIndex), 1, (255,255,255))
            SCREEN.blit(text, (10, 10))
            SCREEN.blit(score_text, (1280-100, 10))
            SCREEN.blit(level_text, (1280//2, 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()
