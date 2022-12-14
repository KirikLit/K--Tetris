import json
import random

class Shape():
    def __init__(self, field, shape):
        # setup
        self.field = field
        
        # set shape
        self.shape = shape

        # coordinates
        self.x = 3
        self.y = self._upAsPossible()
    
    def update(self):
        # insert ghost shape if enabled in settings.json
        if self.field.ghostShape:
            self.insertGhost()
        
        # insert shape to the field
        self.insert(self.x, self.y)

    def insert(self, posX, posY, field=None, shape=None):
        field = self.field.field if field is None else field
        shape = self.shape if shape is None else shape
        for iy, y in enumerate(shape):
            for ix, x in enumerate(y):
                if x:
                    field[iy + posY][ix + posX] = x

    def insertGhost(self):
        posY = self._downAsPossible()

        for iy, y in enumerate(self.shape):
            for ix, x in enumerate(y):
                if x:
                    self.field.field[iy + posY][ix + self.x] = 8
    
    def drop(self):
        self.y = self._downAsPossible()

    def tryToInsert(self, posX, posY, shape=None):
        # try to insert shape in field
        shape = self.shape if shape is None else shape
        try:
            for iy, y in enumerate(shape):
                for ix, x in enumerate(y):
                    if (x and self.field.nonPlayShapes[iy + posY][ix + posX]) or (x and ((iy + posY < 0) or (ix + posX < 0))):
                        return False
            return True
        except IndexError:
            return False

    def move(self, moveX, moveY):
        # move shape
        if self.tryToInsert(self.x + moveX, self.y):
            self.x += moveX

        if self.tryToInsert(self.x, self.y + moveY):
            self.y += moveY

    def rotate(self):
        # get rotated shape
        rotatedShape = self._rotateClockwise()

        # move rotated
        for move in ((0,0), (1, 0), (-1, 0)):
            if self.tryToInsert(self.x + move[0], self.y + move[1], rotatedShape):
                self.x += move[0]
                self.y += move[1]
                self.shape = rotatedShape
                # return if finded position
                return
    
    def _getHeight(self):
        # copy of shape
        shape = self.shape.copy()

        # exclude empty lines
        for i, line in enumerate(shape):
            if not any(line):
                shape.pop(i)
        
        # return height
        return len(shape)

    def _rotateClockwise(self):
        rotated = []
        for x in range(len(self.shape[0])):
            temp = []
            for y in range(len(self.shape)):
                temp.insert(0, self.shape[y][x])
            rotated.append(temp)
        return rotated
    
    def _upAsPossible(self):
        for y in range(-3, 1, 1):
            if self.tryToInsert(self.x, y):
                return y
        self.field.gameOver()
        return False

    def _downAsPossible(self):
        maxY = 0
        for y in range(20):
            if self.tryToInsert(self.x, y):
                maxY = y
            else:
                return maxY
        return False
        