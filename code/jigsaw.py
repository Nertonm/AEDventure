#!/usr/bin/env python

import pygame
import sys
import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_q, MOUSEBUTTONDOWN

# Exit
def terminate():
    pygame.quit()
    sys.exit()

class Jigsaw:

    # Initialize the jigsaw's size
    # And generate a new game board randomly
    def __init__(self, vhNum):
        self.vhNum = vhNum
        self.cellNum = vhNum * vhNum

        self.board = []
        for i in range(self.cellNum):
            self.board.append(i)
        random.shuffle(self.board)

        self.whiteCell = self.board.index(self.cellNum - 1)


    # Check if it can be done or not
    def isResolvable(self):
        inversion = 0
        whiteDistance = (self.vhNum - 1) - self.whiteCell // self.vhNum

        tmp = []
        for i in range(self.cellNum):
            tmp.append(self.board[i])
        del tmp[self.whiteCell]

        for i in range(len(tmp)):
            for j in range(i + 1, len(tmp)):
                if tmp[i] > tmp[j]:
                    inversion += 1

        if self.vhNum % 2 != 0:
            return inversion % 2 == 0

        return (inversion % 2 == 0) == (whiteDistance % 2 == 0)


    # Have it done?
    def isFinish(self):
        for i in range(self.cellNum):
            if i != self.board[i]:
                return False
        return True

def runGame(vhNum):
    pygame.init()

    gameImage = pygame.image.load("00%d.png" % vhNum)

    gameRect = gameImage.get_rect()
    screen = pygame.display.set_mode((gameRect.width, gameRect.height))
    pygame.display.set_caption("%s*%s Jigsaw Puzzle" % (vhNum, vhNum))

    gameBoard = Jigsaw(vhNum)
    while not gameBoard.isResolvable():
        gameBoard = Jigsaw(vhNum)

    whiteCell = int(gameBoard.whiteCell)

    cellNum = vhNum * vhNum
    cellWidth = gameRect.width // vhNum
    cellHeight = gameRect.height // vhNum

    while True:

        if gameBoard.isFinish() and vhNum < 5:
            runGame(vhNum + 1)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    terminate()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                row = y // cellHeight
                col = x // cellWidth
                index = int(row * vhNum + col)
                if (index == whiteCell - vhNum or index == whiteCell + vhNum
                        or (whiteCell % vhNum != vhNum - 1 and index == whiteCell + 1)
                        or (whiteCell % vhNum != 0 and index == whiteCell - 1)):
                    gameBoard.board[index], gameBoard.board[whiteCell] = gameBoard.board[whiteCell], gameBoard.board[index]
                    whiteCell = index

        for i in range(vhNum):
            pygame.draw.line(gameImage, (0, 0, 0), (0, i * cellHeight), (gameRect.width, i * cellHeight))
            pygame.draw.line(gameImage, (0, 0, 0), (cellWidth * i, 0), (cellWidth * i, gameRect.height))

        for i in range(cellNum):
            rowDst = i // vhNum
            colDst = i % vhNum
            rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)

            rowSrc = gameBoard.board[i] // vhNum
            colSrc = gameBoard.board[i] % vhNum
            rectSrc = pygame.Rect(colSrc * cellWidth, rowSrc * cellHeight, cellWidth, cellHeight)

            screen.blit(gameImage, rectDst, rectSrc)

        pygame.display.update()

runGame(3)