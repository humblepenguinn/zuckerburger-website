import pygame

TOWER_HEIGHT = 400
TOWER_WIDTH = 30

TILE_HEIGHT = 30
TILE_WIDTH = 100

NUM_TILES = 3

TILE_COLOR = (190, 120, 0)
HOVER_TILE_COLOR = (190, 120, 255)

TOWER_COLOR = (255, 255, 255)
HOVER_TOWER_COLOR = (123, 230, 98)

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

    def Update(self, game):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and game.currentlyDraggingTile != None and game.currentlyDraggingTile.tower != self and game.CanMoveTileToTower(game.currentlyDraggingTile, self):
            self.color = HOVER_TOWER_COLOR
        else:
            self.color = TOWER_COLOR

        for tile in self.tiles:
            tile.Update()

    def Render(self):
        pygame.draw.rect(self.main_screen, self.color, self.rect)

        #self.main_screen.blit(self.image, self.rect)

        i = len(self.tiles) - 1
        for tile in self.tiles:
            if not tile.isBeingDragged:
                tile.Render((self.x_position, -(i * (TILE_HEIGHT + 10)) + self.rect.bottom))

            i -= 1


class Tile:

    def __init__(self, main_screen: pygame.Surface, tower: Tower, width) -> None:
        self.main_screen = main_screen
        self.tower = tower
        self.width = width
        self.color = TILE_COLOR

        self.image = pygame.image.load("assets/images/Bar2.png")
        self.image = pygame.transform.scale(self.image, (width, TILE_HEIGHT))
        self.image.fill(TILE_COLOR, special_flags=pygame.BLEND_ADD)

        self.rect = pygame.Rect(self.tower.x_position, self.tower.y_position, width, TILE_HEIGHT)
        self.rect.center = (self.tower.x_position, self.tower.y_position)
        
        self.isBeingDragged = False

    def MoveToTower(self, tower):
        self.tower = tower
        self.rect = pygame.Rect(self.tower.x_position, self.tower.y_position, self.width, TILE_HEIGHT)
        self.rect.center = (self.tower.x_position, self.tower.y_position)

    def OnEvent(self, event):
        pass

    def Update(self):
        # Check if mouse is over rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = HOVER_TILE_COLOR
        else:
            self.color = TILE_COLOR

    def Render(self, centerPos):
        if self.tower is None:
            return

        self.rect.center = centerPos

        pygame.draw.rect(self.main_screen, self.color, self.rect)
        #self.main_screen.blit(self.image, self.rect)


class TowerOfHanoi:

    def __init__(self, main_screen: pygame.Surface):
        self.main_screen = main_screen
        self.width = main_screen.get_width()
        self.height = main_screen.get_height()
        self.towers = []
        self.tiles = []
        self.currentlyDraggingTile = None

        difference = self.width / 4

        for i in range(1, 4):
            xPos =  (difference * i)
            tower = Tower(self.main_screen, xPos, self.height - (TOWER_HEIGHT / 2) - 100)
            self.towers.append(tower)

        for i in range(NUM_TILES):
            tile = Tile(self.main_screen, self.towers[0], TILE_WIDTH + (i * TILE_WIDTH))
            self.tiles.append(tile)
            self.towers[0].AddTile(tile)

    def GetTowerForTile(self, tile):
        for tower in self.towers:
            for towerTile in tower.tiles:
                if towerTile == tile:
                    return tower

    def MoveTileToTower(self, tile, tower):
        currentTower = self.GetTowerForTile(tile)

        if currentTower == None:
            return

        tile.MoveToTower(tower)
        currentTower.RemoveTile(tile)
        tower.AddTile(tile, True)

    def CanMoveTileToTower(self, tile, tower):
        if len(tower.tiles) == 0:
            return True

        # Get the topmost tile of the tower
        topmostTile = tower.tiles[0]

        if topmostTile == None:
            return True

        if tile.width < topmostTile.width:
            return True

        return False

    def OnEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.currentlyDraggingTile == None:
            # Find the tile clicked on
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    self.currentlyDraggingTile = tile
                    self.currentlyDraggingTile.isBeingDragged = True
                    break

        elif event.type == pygame.MOUSEBUTTONUP and self.currentlyDraggingTile != None:
            # Find the tower the mouse is on 
            for tower in self.towers:
                if tower.rect.collidepoint(pygame.mouse.get_pos()) and self.CanMoveTileToTower(self.currentlyDraggingTile, tower):
                    self.MoveTileToTower(self.currentlyDraggingTile, tower)
                    break
                

            self.currentlyDraggingTile.isBeingDragged = False
            self.currentlyDraggingTile = None

        for tower in self.towers:
            tower.OnEvent(event)

    def Update(self):
        for tower in self.towers:
            tower.Update(self)

    def Render(self):
        for tower in self.towers:
            tower.Render()

        if self.currentlyDraggingTile != None:
            self.currentlyDraggingTile.Render(pygame.mouse.get_pos())
