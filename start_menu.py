import pygame

from game import Game
from utils import *

class StartMenu(Game):
    def __init__(self, main_screen: pygame.Surface, timer: pygame.time.Clock) -> None:
        super().__init__(main_screen, timer)

        self.greeting_font = get_font(100)
        self.greeting_text = self.greeting_font.render("Zuckerberg's IDE", True, (255, 255, 255))
        self.greeting_text_rect = self.greeting_text.get_rect(center=(self.main_screen.get_width() / 2, self.main_screen.get_height() * 0.15))

        self.prompt_text_font = get_font(30)
        self.prompt_text = self.prompt_text_font.render("Enter your HC ID and password and click START!", True, (255, 255, 255))
        self.prompt_text_rect = self.prompt_text.get_rect(center=(self.main_screen.get_width() / 2, (self.main_screen.get_height() / 2) - 100))

        self.hc_input_box = InputBox((self.main_screen.get_width() / 2, self.main_screen.get_height() / 2), 50)
        self.password_input_box = InputBox((self.main_screen.get_width() / 2, (self.main_screen.get_height() / 2) + 80), 50, isPassword=True)

    def OnEvent(self, event: pygame.event.Event):
        super().OnEvent(event)

        self.hc_input_box.OnEvent(event)
        self.password_input_box.OnEvent(event)

    def Update(self, dt):
        super().Update(dt)


    def Render(self):
        super().Render()
        self.main_screen.fill((0, 0, 0))

        self.main_screen.blit(self.greeting_text, self.greeting_text_rect)
        self.main_screen.blit(self.prompt_text, self.prompt_text_rect)
        self.hc_input_box.Render(self.main_screen)
        self.password_input_box.Render(self.main_screen)
