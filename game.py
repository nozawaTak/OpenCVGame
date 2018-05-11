import cv2
from bear import Bear
from card import Card
from enemy import Enemy
from collisionWatcher import CollisionWatcher
import random
import numpy as np
from scipy import ndimage


class Game():
    def __init__(self, level=1):
        cv2.namedWindow('PlayGame', cv2.WINDOW_AUTOSIZE)
        self.level = level
        if self.level == 1:
            pathBackGround = 'imgsrc/resizedforrest.png'
            pathHoney = 'imgsrc/TransparentHoney.png'
            pathHero = 'imgsrc/Transparentpooh.png'
            pathEnemy = 'imgsrc/bee.png'
        elif self.level == 2:
            pathBackGround = 'imgsrc/resizedforrest.png'
            pathHoney = 'imgsrc/TransparentHoney.png'
            pathHero = 'imgsrc/Transparentpooh.png'
            pathEnemy = 'imgsrc/bee.png'
        elif self.level == 3:
            pathBackGround = 'imgsrc/resizedmap.png'
            pathHoney = 'imgsrc/comic1.png'
            pathHero = 'imgsrc/Transparentbear.png'
            pathEnemy = 'imgsrc/resizedpolice.png'
            self.value = [0, 260, 280, 280, 620, 270, 380, 590]

        self.backGround = cv2.imread(pathBackGround)
        self.honey = cv2.imread(pathHoney, -1)
        self.hero = cv2.imread(pathHero, -1)
        self.enemy = cv2.imread(pathEnemy, -1)

        self.windowSize = self.backGround.shape[:2]
        self.copy = self.backGround.copy()
        cv2.rectangle(self.copy, (695, 0), (self.windowSize[1], 35), (255, 255, 255), -1)
        self.collisionWatcher = CollisionWatcher(self.windowSize)
        self.bear = Bear(900, 400, self.hero)
        self.bee = Enemy(100, 100, self.enemy)
        self.cards = []
        self.collisionWatcher.setBear(self.bear)
        self.collisionWatcher.setEnemy(self.bee)
        self.collisionWatcher.setCards(self.cards)

    def drawItem(self, frame, Item):
        posX, posY = Item.getPosition()[:2]
        img = Item.getImg()
        height, width = img.shape[:2]
        height //= 2
        width //= 2
        if Item.getMask() is not None:
            mask = Item.getMask()
            frame[posY-height:posY+height, posX-width:posX+width] *= 1 - mask
            frame[posY-height:posY+height, posX-width:posX+width] += img * mask
        else:
            frame[posY-height:posY+height, posX-width:posX+width] = img
        if self.level == 1 and isinstance(Item, Bear):
            frame = self.mosaic_area(frame, posX-width, posY-height, width*2, height*2)


    def generateHoney(self):
        if self.level == 3:
            num = random.randint(1, 7)
            path = 'imgsrc/comic/comic' + str(num) + '.png'
            self.honey = cv2.imread(path)
            heightHoney, widthHoney = self.honey.shape[:2]
            heiH = heightHoney // 2
            widH = widthHoney // 2
            posX = random.randint(widH, self.windowSize[1]-widH)
            posY = random.randint(heiH, self.windowSize[0]-heiH)
            self.cards.append(Card(posX, posY, self.honey, self.level, point=self.value[num]))
        else :
            heightHoney, widthHoney = self.honey.shape[:2]
            heiH = heightHoney // 2
            widH = widthHoney // 2
            posX = random.randint(widH, self.windowSize[1]-widH)
            posY = random.randint(heiH, self.windowSize[0]-heiH)
            self.cards.append(Card(posX, posY, self.honey, self.level))



    def gameOver(self, frame):
        i = 0
        while i < 35:
            bg = frame.copy()
            Irot = ndimage.rotate(self.bear.getImg(), i, reshape=False)
            Mrot = ndimage.rotate(self.bear.getMask(), i, reshape=False)
            self.bear.setImg(Irot)
            self.bear.setMask(Mrot)
            self.drawItem(bg, self.bear)
            cv2.imshow('PlayGame', bg)
            cv2.waitKey(1)
            i += 1

        if self.level != 3:
            x, y = self.windowSize[:2]
            x //= 2
            y //= 2
            cv2.rectangle(self.backGround, (0, 0), (960, 544), (255, 119, 103), -1)
            overImg = cv2.imread('imgsrc/TransparentpoohGameOver.png')
            width, height = overImg.shape[:2]
            self.backGround[80:80+width, 50:50+height] = overImg
            cv2.putText(self.backGround, 'Game Over', (x-100, y-200),
                            cv2.FONT_HERSHEY_COMPLEX, 3, (0,0,0), thickness=4)
            cv2.putText(self.backGround, 'Points: ' + str(self.bear.getHavingPoint()), (x, y),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), thickness=3)
            while True:
                cv2.imshow('PlayGame', self.backGround)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    return 'end'
                elif cv2.waitKey(1) & 0xff == ord('r'):
                    return ''
        else:
            x, y = self.windowSize[:2]
            x //= 2
            y //= 2
            cv2.rectangle(self.backGround, (0, 0), (960, 544), (255, 119, 103), -1)
            cv2.putText(self.backGround, 'Game Over', (x-100, y-200),
                            cv2.FONT_HERSHEY_COMPLEX, 3, (0,0,0), thickness=4)
            cv2.putText(self.backGround, 'Points: ' + str(self.bear.getHavingPoint()), (x, y),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), thickness=3)
            while True:
                cv2.imshow('PlayGame', self.backGround)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    return 'end'
                elif cv2.waitKey(1) & 0xff == ord('r'):
                    return ''

    def mosaic(self, src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def mosaic_area(self, src, x, y, width, height, ratio=0.1):
        dst = src
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width], ratio)
        return dst

    def operate(self):
        cap = cv2.VideoCapture(0)
        # cv2.namedWindow('hand', cv2.WINDOW_NORMAL)
        message = ''
        low = np.array([0, 30, 60])
        high = np.array([20, 150, 255])
        kernel = np.ones((5,5), np.uint8)
        while True:
            frame = self.copy.copy()
            if len(self.cards) < 30 and random.randint(0, 100) > 98:
                self.generateHoney()
            if cap.isOpened():
                ret, img = cap.read()
                img = cv2.flip(img, 1)
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                skin = cv2.inRange(hsv, low, high)
                advance = cv2.dilate(skin,kernel)
                advance = cv2.erode(advance,kernel)
                _, contours, hierarchy = cv2.findContours(advance, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                if len(contours) > 0:
                    index = 0
                    max = 0
                    for i in range(0, len(contours)):
                        area = cv2.contourArea(contours[i])
                        if area > max:
                            index = i
                            max = area
                    # cv2.drawContours(img, contours, index, (0, 0, 255), 2, 8, hierarchy, 0)
                    lrtb = []
                    cnt = contours[index]
                    lrtb.append(tuple(cnt[cnt[:,:,0].argmin()][0]))
                    lrtb.append(tuple(cnt[cnt[:,:,0].argmax()][0]))
                    lrtb.append(tuple(cnt[cnt[:,:,1].argmin()][0]))
                    lrtb.append(tuple(cnt[cnt[:,:,1].argmax()][0]))
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cg = np.array([cx, cy])
                    max = 0
                    index = 0
                    for i, point in enumerate(lrtb):
                        b = np.array(point)
                        norm = np.linalg.norm(b - cg)
                        if norm > max:
                            max = norm
                            index = i
                    # cv2.circle(img, (cx ,cy), 20, (0,255,0), -1)
                    # cv2.circle(img, lrtb[index], 20, (255,0,0), -1)
                    # cv2.imshow('hand', img)
                    x = lrtb[index][0] - cx
                    y = lrtb[index][1] - cy
                    if x >= 0 and y >= 0:
                        if x < y:
                            ope =  'bottom'
                        else:
                            ope =  'right'
                    elif x >= 0 and y < 0:
                        if x < abs(y):
                            ope =  'top'
                        else:
                            ope = 'right'
                    elif x < 0 and y >= 0:
                        if abs(x) < y:
                            ope = 'bottom'
                        else:
                            ope = 'left'
                    else:
                        if abs(x) < abs(y):
                            ope = 'top'
                        else:
                            ope = 'left'
                    self.bear.opePosition(ope)
            self.bee.calPosition()
            self.collisionWatcher.watch()
            if self.collisionWatcher.collideEnemy():
                for card in self.cards:
                    self.drawItem(frame, card)
                self.drawItem(frame, self.bee)
                message = self.gameOver(frame)
                break
            else:
                for card in self.cards:
                    self.drawItem(frame, card)
                self.drawItem(frame, self.bee)
                self.drawItem(frame, self.bear)
                if self.level == 3:
                    cv2.putText(frame, 'Money: '+ str(self.bear.getHavingPoint()), (700, 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), thickness=3)
                else :
                    cv2.putText(frame, 'Points: ' + str(self.bear.getHavingPoint()), (700, 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), thickness=3)
                cv2.imshow('PlayGame', frame)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
        return message

    def run(self):
        message = ''
        while True:
            frame = self.copy.copy()
            if len(self.cards) < 30 and random.randint(0, 100) > 98:
                self.generateHoney()

            self.bear.calPosition()
            self.bee.calPosition()
            self.collisionWatcher.watch()
            if self.collisionWatcher.collideEnemy():
                message = self.gameOver()
                break
            else:
                for card in self.cards:
                    self.drawItem(frame, card)

                self.drawItem(frame, self.bee)
                self.drawItem(frame, self.bear)

                if self.level == 3:
                    cv2.putText(frame, '¥ '+ str(self.bear.getHavingPoint()), (700, 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), thickness=3)
                else :
                    cv2.putText(frame, 'Points: ' + str(self.bear.getHavingPoint()), (700, 30),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), thickness=3)
                cv2.imshow('PlayGame', frame)
                if cv2.waitKey(5) & 0xff == ord('q'):
                    break
        return message
