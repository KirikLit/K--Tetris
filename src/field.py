import pygame
import json
from src.shape import Shape

class Field():
    SHAPE_SIZE = 16

    def __init__(self):
        # setup
        self.field = [[0 for i in range(10)] for i in range(20)]
        self.nonPlayShapes = [[0 for i in range(10)] for i in range(20)]
        self.surface = pygame.Surface((160, 320))

        # setup timers
        self.moveYDelay = 15
        self.moveYTimer = 0

        self.playerMoveDelay = 3
        self.playerMoveTimer = 0

        # image
        self.block = pygame.image.load('src/res/block.png')
        self.blockRect = self.block.get_rect()

        # create first shape
        self.createShape()

    def update(self, events):
        # timers 
        self.moveYTimer += 1
        self.playerMoveTimer += 1

        # clear field
        self.field = [[0 for i in range(10)] for i in range(20)]
        self._pasteNonPlayShapes()

        # shape update
        if self.moveYTimer >= self.moveYDelay:
            if not self.playerShape.tryToInsert(self.playerShape.x, self.playerShape.y + 1):
                self.pasteShape()
            self.moveYTimer = 0
            self.playerShape.move(0, 1)
        
        if (events['left'] or events['right'] or events['down']) and self.playerMoveTimer >= self.playerMoveDelay:
            self.playerMoveTimer = 0
            self.playerShape.move(events['right'] - events['left'], events['down'])
        
        if events['rotate']:
            self.playerShape.rotate()
            events['rotate'] = False

        self.playerShape.update()

        # field
        # draw
        self.drawField()

        # clear full row
        for i, line in enumerate(self.nonPlayShapes):
            if all(line):
                self.nonPlayShapes.pop(i)
                self.nonPlayShapes.insert(0, [0 for i in range(10)])
        self._pasteNonPlayShapes()        
        

        return self.surface

    def drawField(self):
        # clear surface
        self.surface.fill((0,0,0))

        # draw
        light = False
        for iy, y in enumerate(self.field):
            for ix, x in enumerate(y):
                if x:
                    # pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(ix * self.SHAPE_SIZE, iy * self.SHAPE_SIZE, self.SHAPE_SIZE, self.SHAPE_SIZE))
                    self.surface.blit(self.colorizedBlock(x), (ix * self.SHAPE_SIZE, iy * self.SHAPE_SIZE))
                elif light:
                    pygame.draw.rect(self.surface, (25, 25, 25), pygame.Rect(ix * self.SHAPE_SIZE, iy * self.SHAPE_SIZE, self.SHAPE_SIZE, self.SHAPE_SIZE))
                light = not light
            light = not light
    
    def createShape(self):
        self.playerShape = Shape(self)

    def colorizedBlock(self, color):
        # get colors from json
        with open('src/shapes.json') as f:
            colors = json.load(f)['colors']
            f.close()
        
        # colorize block
        block = self.block.copy()
        colorBlock = pygame.Surface(block.get_size()).convert_alpha()
        colorBlock.fill(colors[color])
        block.blit(colorBlock, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

        return block

    def gameOver(self):
        # setup new game
        self.field = [[0 for i in range(10)] for i in range(20)]
        self.nonPlayShapes = [[0 for i in range(10)] for i in range(20)]
        self.createShape()

        self.moveYTimer = 0
        self.playerMoveTimer = 0
        

    def pasteShape(self):
        # insert shapa to nonPlayShapes list
        self.playerShape.insert(self.playerShape.x, self.playerShape.y, self.nonPlayShapes)

        # create new shape
        self.createShape()

        # update field with new nonPlayShapes
        self._pasteNonPlayShapes()

    def _pasteNonPlayShapes(self):
        # mix field with nonPlayShapes
        for iy, y in enumerate(self.nonPlayShapes):
            for ix, x in enumerate(y):
                if x:
                    self.field[iy][ix] = x
    