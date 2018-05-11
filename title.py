import cv2
from game import Game
from PIL import Image, ImageDraw, ImageFont
from mouseEvent import MouseEvent
import numpy as np

class Title():
    def __init__(self):
        self.windowName = 'PlayGame'
        cv2.namedWindow(self.windowName, cv2.WINDOW_AUTOSIZE)
        self.mouse = MouseEvent(self.windowName)
        self.backGround = cv2.imread('imgsrc/resizedforrest.png')

    def drawJapanese(self, img, text, x, y, size=27, color=(255, 0, 0)):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        PIL_data = Image.fromarray(img)
        draw = ImageDraw.Draw(PIL_data)
        font = ImageFont.truetype("/Users/nozawa/Library/fonts/TanukiMagic.ttf", size)
        draw.text((x, y), text, fill=color, font=font)
        CV_data = np.asarray(PIL_data)
        image = cv2.cvtColor(CV_data, cv2.COLOR_RGB2BGR)
        return image

    def start(self):
        recsize = [125, 45]
        w, h = recsize[:2]
        x1 = 420
        y1 = 400
        bg = self.backGround.copy()
        cv2.ellipse(bg, (480, 150), (300, 100), 0, 0, 360, (59, 95, 165), -1)
        cv2.ellipse(bg, (480, 150), (300, 100), 0, 0, 360, (0, 0, 0), 2)
        cv2.rectangle(bg, (x1, y1), (x1+w, y1+h), (255, 255, 255), -1)
        cv2.rectangle(bg, (x1, y1), (x1+w, y1+h), (0,0,0))
        bg = self.drawJapanese(bg, u'はじめる', x1+10, y1+10)
        bg = self.drawJapanese(bg, u'くまさんのはちみつ狩り', 220, 125, size=50, color=(255, 251, 38))
        while True:
            cv2.imshow('PlayGame', bg)
            if self.mouse.getEvent() == cv2.EVENT_LBUTTONDOWN:
                x = self.mouse.getX()
                y = self.mouse.getY()
                if x1 < x and x < x1+w :
                    if y1 < y and y < y1+h:
                        return ''
            if cv2.waitKey(1) & 0xff == ord('q'):
                return None


    def select(self):
        recsize = [250, 45]
        w, h = recsize[:2]
        x1 = 325
        y1 = 160
        y2 = 240
        y3 = 320
        bg = cv2.medianBlur(self.backGround, 9)
        cv2.rectangle(bg, (x1, y1), (x1+w, y1+h), (255, 255, 255), -1)
        cv2.rectangle(bg, (x1, y1), (x1+w, y1+h), (0,0,0))
        cv2.rectangle(bg, (x1, y2), (x1+w, y2+h), (255, 255, 255), -1)
        cv2.rectangle(bg, (x1, y2), (x1+w, y2+h), (0,0,0))
        cv2.rectangle(bg, (x1, y3), (x1+w, y3+h), (255, 255, 255), -1)
        cv2.rectangle(bg, (x1, y3), (x1+w, y3+h), (0,0,0))
        bg = self.drawJapanese(bg, u'著作権を気にする', x1+10, y1+10)
        bg = self.drawJapanese(bg, u'著作権を気にしない', x1+10, y2+10)
        bg = self.drawJapanese(bg, u'もう何も怖くない', x1+10, y3+10)
        while True:
            cv2.imshow('PlayGame', bg)
            if self.mouse.getEvent() == cv2.EVENT_LBUTTONDOWN:
                x = self.mouse.getX()
                y = self.mouse.getY()
                if x1 < x and x < x1+w :
                    if y1 < y and y < y1+h:
                        game = Game(level=1)
                        break
                    elif y2 < y and y < y2+h:
                        game = Game(level=2)
                        break
                    elif y3 < y and y < y3+h:
                        game = Game(level=3)
                        break
            if cv2.waitKey(1) & 0xff == ord('q'):
                game = None
                break
        return game


    def run(self):
        mes = self.start()
        if mes is None:
            game = None
        else :
            game = self.select()
        return game
