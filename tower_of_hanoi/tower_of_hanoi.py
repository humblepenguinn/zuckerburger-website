import pygame
import pygame.math
import datetime

from utils import get_font, InputBox
from game import Game

from tower_of_hanoi.globals import *
from tower_of_hanoi.tower import Tower
from tower_of_hanoi.tile import Tile

class TowerOfHanoi(Game):

    def __init__(self, main_screen: pygame.Surface, timer: pygame.time.Clock):
        super().__init__(main_screen, timer)

        self.width = main_screen.get_width()
        self.height = main_screen.get_height()
        self.towers = []
        self.tiles = []
        self.currentlyDraggingTile = None
        
        self.totalTimeRemaining = datetime.timedelta(minutes=5)
        self.timerText = get_font(100).render(str(self.totalTimeRemaining)[2:7], True, (255, 255, 255))
        self.timerTextRect = self.timerText.get_rect(center=(200, 100))
        self.started = False

        self.gameOver = False
        self.won = False
        self.numOfMovesTaken = 0

        self.InitTowers()

    def InitTowers(self):
        # Some calculations for where to position the 3 towers
        difference = (self.width - 100) / 3
        for i in range(3):
            xPos = (self.width / 2) + ((i - 1) * difference)
            print(xPos)
            tower = Tower(self.main_screen, (xPos, self.height - (TOWER_HEIGHT / 2) - 100))
            self.towers.append(tower)

        # Add all tiles dynamically to the first tower
        for i in range(NUM_TILES):
            tile = Tile(self.main_screen, TILE_WIDTH + (i * TILE_WIDTH))
            self.tiles.append(tile)
            self.towers[0].AddTile(tile)

    def GetTowerForTile(self, tile: Tile) -> Tower:
        for tower in self.towers:
            for towerTile in tower.tiles:
                if towerTile == tile:
                    return tower

    def MoveTileToTower(self, tile: Tile, tower: Tower):
        currentTower = self.GetTowerForTile(tile)

        if currentTower == None:
            return

        currentTower.RemoveTile(tile)
        tower.AddTile(tile, True)

        if not self.started:
            self.started = True 

        self.numOfMovesTaken += 1

    def CanMoveTileToTower(self, tile: Tile, tower: Tower):
        # If there are no tiles on the tower, means can move to that tower
        if len(tower.tiles) == 0:
            return True

        # Get the topmost tile of the tower
        topmostTile = tower.tiles[0]

        if topmostTile == None:
            return True

        # If the tile being moved is smaller than the topmost tile on the tower being moved to
        # then the move is valid
        if tile.width < topmostTile.width:
            return True

        return False

    def OnEvent(self, event: pygame.event.Event):
        if self.gameOver:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and self.currentlyDraggingTile == None:
            # Find the tile clicked on
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()) and self.GetTowerForTile(tile).tiles[0] == tile:
                    self.currentlyDraggingTile = tile
                    self.currentlyDraggingTile.StartDrag()
                    break

        elif event.type == pygame.MOUSEBUTTONUP and self.currentlyDraggingTile != None:
            # Find the tower the mouse is on 
            for tower in self.towers:
                if tower.rect.collidepoint(pygame.mouse.get_pos()) and self.CanMoveTileToTower(self.currentlyDraggingTile, tower):
                    self.MoveTileToTower(self.currentlyDraggingTile, tower)
                    break

            self.currentlyDraggingTile.EndDrag()
            self.currentlyDraggingTile = None

        for tower in self.towers:
            tower.OnEvent(event)

    def GetCurrentGameState(self):
        # Check if you have time remaining
        if self.totalTimeRemaining <= datetime.timedelta(0):
            return True, False

        # Check in the second and third tower
        # if either of them have all the tiles on them
        # If they do, game won
        for i in range(1, 3):
            tower = self.towers[i]
            if len(tower.tiles) == NUM_TILES:
                return True, True

        return False, False

    def Update(self, dt: float):
        if self.gameOver:
            return self.gameOver, self.won, self.numOfMovesTaken

        # Update all 3 towers and each of its childs
        for tower in self.towers:
            tower.Update(dt, self)
        
        # GetCurrentGameState returns a tuple 
        # with 2 bools, game over and game won
        (gameOver, gameWon) = self.GetCurrentGameState()

        # If game is over, return out of the functions
        if gameOver and not self.gameOver:
            self.gameOver = True
            self.won = gameWon

            if self.currentlyDraggingTile != None:
                self.currentlyDraggingTile.isBeingDragged = False
                self.currentlyDraggingTile = None

            return self.gameOver, self.won, self.numOfMovesTaken

        if self.started:
            # Decrease our time remaining each frame
            self.totalTimeRemaining -= datetime.timedelta(seconds=dt)

            # Makes sure that even if the time remaining goes below 0, it will still display 0 on our text
            if self.totalTimeRemaining <= datetime.timedelta(0):
                self.totalTimeRemaining = datetime.timedelta(0)

        return False, False, self.numOfMovesTaken

    def Render(self):
        # Render the time remaining text with some formatting
        self.timerText = get_font(100).render(str(self.totalTimeRemaining)[2:7], True, (255, 255, 255))
        # Renders the timer text to the screen
        self.main_screen.blit(self.timerText, self.timerTextRect)

        # Renders all 3 towers and each of its tiles
        for tower in self.towers:
            tower.Render()

        # Separate rendering for tile being dragged
        if self.currentlyDraggingTile != None:
            self.currentlyDraggingTile.Render()
