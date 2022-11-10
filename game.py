import pygame

class Game:
    def __init__(self, main_screen: pygame.Surface, timer: pygame.time.Clock):
        self.timer = timer
        self.main_screen = main_screen

    def OnEvent(self, event: pygame.event.Event):
        pass

    def Update(self, dt):
        pass

    def Render(self):
        pass