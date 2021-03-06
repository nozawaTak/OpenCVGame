from circle import Circle
import random
import cv2

class Enemy(Circle):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.radius = 5
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy =0
        self.vxLimit = 5
        self.vyLimit = 5
        self.img = img
        self.mask = None
        self.makeMask()

    def getImg(self):
        return self.img

    def randAcceleration(self):
        self.ax = random.randint(-1, 1)
        self.ay = random.randint(-1, 1)

    def getHavingPoint(self):
        return self.havingPoint

    def calVelocity(self):
        self.vx += self.ax
        self.vy += self.ay
        if self.vx > self.vxLimit:
            self.vx = self.vxLimit
        if self.vy > self.vyLimit:
            self.vy = self.vyLimit

    def calPosition(self):
        self.randAcceleration()
        self.calVelocity()
        self.x += self.vx
        self.y += self.vy

    def xbound(self, *argv):
        if len(argv) > 0:
            self.x = argv[0]
        self.vx = -self.vx

    def ybound(self, *argv):
        if len(argv) > 0:
            self.y = argv[0]
        self.vy = -self.vy

    def makeMask(self):
        mask = self.img[:,:,3]
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) # 3色分に増やす。
        self.mask = mask // 255 # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
        self.img = self.img[:,:,:3] # アルファチャンネルはもういらないので捨てる。

    def getMask(self):
        return self.mask
