import pygame

from tower_of_hanoi.globals import *

class Tile:

    def __init__(self, main_screen: pygame.Surface, width) -> None:
        self.main_screen = main_screen
        self.width = width
        self.color = TILE_COLOR

        self.image = pygame.image.load("assets/images/Bar2.png")
        self.image = pygame.transform.scale(self.image, (width, TILE_HEIGHT))
        self.image.fill(TILE_COLOR, special_flags=pygame.BLEND_ADD)
        
        self.rect = None

        self.isBeingDragged = False

    def StartDrag(self):
        self.isBeingDragged = True

    def EndDrag(self):
        self.isBeingDragged = False
        self.rect.size = (self.width, TILE_HEIGHT)
        self.isBeingDragged = False            

    def HandleDrag(self, dt):
        if not self.isBeingDragged:
            return

        targetSize = pygame.math.Vector2(self.width, TILE_HEIGHT) * 2
        speed = dt * 10
        self.UpdateRect(pygame.mouse.get_pos(), pygame.math.Vector2(self.rect.size).lerp(targetSize, speed))

    def UpdateRect(self, centerPos, size=None):
        if self.rect is None:
            self.rect = pygame.rect.Rect(centerPos, (self.width, TILE_HEIGHT))

        if size is not None:
            self.rect.size = tuple(size)

        self.rect.center = centerPos

    def OnEvent(self, event):
        pass

    def Update(self, dt):
        if self.rect is None:
            return
        
        # Check if mouse is over rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = HOVER_TILE_COLOR
        else:
            self.color = TILE_COLOR

        # Drag stuff
        self.HandleDrag(dt)

    def Render(self):
        pygame.draw.rect(self.main_screen, self.color, self.rect, border_radius=5)
        #self.main_screen.blit(self.image, self.rect)

