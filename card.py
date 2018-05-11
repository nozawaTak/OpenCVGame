from circle import Circle
import cv2

class Card(Circle):
    def __init__(self, x, y, img, level, point=200):
        super().__init__(x, y)
        self.point = point
        self.img = img
        self.mask = None
        if level != 3:
            self.makeMask()

    def makeMask(self):
        mask = self.img[:,:,3]
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) # 3色分に増やす。
        self.mask = mask // 255 # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
        self.img = self.img[:,:,:3] # アルファチャンネルはもういらないので捨てる。

    def getMask(self):
        return self.mask

    def getImg(self):
        return self.img

    def getPoint(self):
        return self.point
