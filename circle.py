import numpy as np

class Circle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20

    def calDistance(self, circle):
        myVec = np.array((self.x, self.y))
        vsVec = np.array(circle.getPosition())
        L = np.linalg.norm(vsVec - myVec)
        return L

    def getPosition(self):
        return (self.x, self.y)

    def getRadius(self):
        return self.radius
