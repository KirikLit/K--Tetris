import json
import random

class Shape():
    def __init__(self, field):
        # setup
        self.field = field
        self.setShape()

        # coordinates
        self.x = 3
        self.y = self._upAsPossible()
    
    def update(self):
        self.insert(self.x, self.y)

    def insert(self, posX, posY, field=None, shape=None):
        field = self.field.field if field is None else field
        shape = self.shape if shape is None else shape
        for iy, y in enumerate(self.shape):
            for ix, x in enumerate(y):
                if x:
                    field[iy + posY][ix + posX] = x

    def setShape(self):
        # get shapes from shapes.json
        with open('src/shapes.json') as f:
            shapes = json.load(f)
            f.close()
        
        # choose shape
        shape = random.choice(shapes['shapes'])
        #shape = shapes['shapes'][6]

        # set shape
        self.shape = shape
        del shape, shapes

    def tryToInsert(self, posX, posY, shape=None):
        shape = self.shape if shape is None else shape
        try:
            for iy, y in enumerate(shape):
                for ix, x in enumerate(y):
                    if (x and self.field.field[iy + posY][ix + posX]) or (x and ((iy + posY < 0) or (ix + posX < 0))):
                        return False
            return True
        except IndexError:
            return False


    def move(self, moveX, moveY):
        if self.tryToInsert(self.x + moveX, self.y):
            self.x += moveX

        if self.tryToInsert(self.x, self.y + moveY):
            self.y += moveY

    def rotate(self):
        rotatedShape = self._rotateClockwise()
        for move in ((0,0), (1, 0), (-1, 0)):
            if self.tryToInsert(self.x + move[0], self.y + move[1], rotatedShape):
                self.x += move[0]
                self.y += move[1]
                self.shape = rotatedShape

                return
            

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
        for y in range(20, -1, -1):
            if self.tryToInsert(self.x, y):
                return y
        