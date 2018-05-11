from circle import Circle
from card import Card
import numpy as np

class CollisionWatcher():
    def __init__(self, windowSize):
        self.height = windowSize[0]
        self.width = windowSize[1]
        self.bear = None
        self.enemy = None
        self.cards = []

    def setBear(self, bear):
        self.bear = bear

    def setEnemy(self, enemy):
        self.enemy = enemy

    def setCards(self, cards):
        self.cards = cards

    def collideWall(self, Item):
        x, y = Item.getPosition()
        img = Item.getImg()
        height, width = img.shape[:2]
        height //= 2
        width //= 2
        if x < width:
            Item.xbound(width)
        elif x > self.width-width:
            Item.xbound(self.width-width)
        if y < height:
            Item.ybound(height)
        elif y > self.height-height:
            Item.ybound(self.height-height)

    def collideCard(self):
        if len(self.cards) > 0:
            for i, card in enumerate(self.cards):
                if self.bear.calDistance(card) < self.bear.getRadius() + card.getRadius():
                    self.bear.getCard(card)
                    self.cards[i] = ''
            while '' in self.cards:
                self.cards.remove('')

    def collideEnemy(self):
        if self.bear.calDistance(self.enemy) < self.bear.getRadius() + self.enemy.getRadius():
            return True

    def watch(self):
        self.collideWall(self.bear)
        self.collideWall(self.enemy)
        self.collideCard()
