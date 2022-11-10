import pygame

from tower_of_hanoi.globals import *

class Tower:
    def __init__(self, main_screen: pygame.Surface, x_position, y_position):
        self.main_screen = main_screen
        self.tiles = []
        self.x_position = x_position
        self.y_position = y_position
        self.color = TOWER_COLOR

        self.rect = pygame.Rect(self.x_position, self.y_position, TOWER_WIDTH, TOWER_HEIGHT)
        self.rect.center = (self.x_position, self.y_position)

        self.image = pygame.image.load("assets/images/Bar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TOWER_WIDTH, TOWER_HEIGHT))

    def AddTile(self, tile, insertAtStart=False):
        if insertAtStart and len(self.tiles) != 0:
            self.tiles.insert(0, tile)
        else:
            self.tiles.append(tile)

    def RemoveTile(self, tile):
        self.tiles.remove(tile)

    def OnEvent(self, event):
        for tile in self.tiles:
            tile.OnEvent(event)

    def Update(self, dt, game):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and game.currentlyDraggingTile != None and game.CanMoveTileToTower(game.currentlyDraggingTile, self):
            self.color = HOVER_TOWER_COLOR
        else:
            self.color = TOWER_COLOR

        i = len(self.tiles) - 1
        for tile in self.tiles:
            if not tile.isBeingDragged:
                tile.UpdateRect((self.x_position, -(i * (TILE_HEIGHT + 10)) + self.rect.bottom))

            tile.Update(dt)
            i -= 1

    def Render(self):
        pygame.draw.rect(self.main_screen, self.color, self.rect, border_radius=10)

        #self.main_screen.blit(self.image, self.rect)

        for tile in self.tiles:
            if not tile.isBeingDragged:
                tile.Render()
