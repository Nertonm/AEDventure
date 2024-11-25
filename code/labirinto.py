# labirinto.py

import pygame,sys
from PIL import Image, ImageDraw
from random import randrange, choice

class Maze:
    def __init__(self, difficult):
        if difficult == 'easy':
            self.tamanho = [4, 4]
        elif difficult == 'medium':
            self.tamanho = [6, 6]
        else:
            self.tamanho = [8, 8]
        #tamanho labirinto
        self.x, self.y = tamanho
        self.caminho = [[self.x * 6 - 3, 3]]
        self.lugares_visitados = [[self.x * 6 - 3, 3]]
        self.linhas = []
        self.pos = {}
        self.id_quadrado = 0
        self.cor = [randrange(15, 255), randrange(15, 255), randrange(15, 255)]
        #tamanho entre linhas e colunas
        self.size = 33
        self.img_new = Image.new('RGBA', (self.x * (self.size + 1) + 1, self.y * (self.size + 1) + 1), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.img_new)
        self.fundo = pygame.image.load("rect.png")
        self.fundo_rect = self.fundo.get_rect(topleft=(0, 0))
        self.img = self.img_new.convert('RGB')
        self.rgb = self.img.load()
        self.img_width, self.img_height = self.img.size
        self.tela = pygame.display.set_mode((800, 600))  # Initialize the tela attribute
        self.move_square = pygame.draw.rect(self.tela, self.cor, ((self.x * self.size - self.size / 2, self.size / 2), (self.size - 1, self.size - 1)))
        self.pos[self.id_quadrado] = [[self.x * self.size - self.size / 2, self.size / 2], self.cor]
        self.tela.blit(self.fundo, self.fundo_rect)

        self.stack = []

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.button_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.buttons = {
            "up": pygame.Rect(50, 400 - 80, 100, 50),
            "down": pygame.Rect(160, 400 - 80, 100, 50),
            "left": pygame.Rect(270, 400 - 80, 100, 50),
            "right": pygame.Rect(380, 400 - 80, 100, 50),
            "enter": pygame.Rect(490, 400 - 80, 100, 50)
        }
        self.button_order = ["up", "down", "left", "right", "enter"]
        self.selected_button = 0

    # Rest of the class methods...

    def fazer_caminho(self):
        while [3, self.y * 6 - 3] not in self.lugares_visitados:
            escolhas = [0, 1, 2, 2, 3, 3]
            xx, yy = self.caminho[-1]
            while True:
                rdm = choice(escolhas)
                escolhas.remove(rdm)
                if rdm == 0:
                    if [xx - 6, yy] not in self.lugares_visitados and xx - 6 > 0:
                        self.lugares_visitados.append([xx - 6, yy])
                        self.caminho.append([xx - 6, yy])
                        break
                elif rdm == 1:
                    if [xx, yy + 6] not in self.lugares_visitados and yy + 6 < self.y * 6:
                        self.lugares_visitados.append([xx, yy + 6])
                        self.caminho.append([xx, yy + 6])
                        break
                elif rdm == 2:
                    if [xx + 6, yy] not in self.lugares_visitados and xx + 6 < self.x * 6:
                        self.lugares_visitados.append([xx + 6, yy])
                        self.caminho.append([xx + 6, yy])
                        break
                else:
                    if [xx, yy - 6] not in self.lugares_visitados and yy - 6 > 0:
                        self.lugares_visitados.append([xx, yy - 6])
                        self.caminho.append([xx, yy - 6])
                        break
        print(self.lugares_visitados)
        print(self.caminho)
        return self.caminho

    def esquerda(self):
        x, y = self.pos[self.id_quadrado][0]
        if x - self.size // 2 >= 0:
            r, g, b = self.rgb[x - self.size // 2, y]
            jogou = False
            if r == 0:
                jogou = True
                self.pos[self.id_quadrado][0][0] -= self.size
            return self.pos, jogou
        return self.pos, False

    def direita(self):
        x, y = self.pos[self.id_quadrado][0]
        if x + self.size // 2 < self.img_width:
            r, g, b = self.rgb[x + self.size // 2, y]
            jogou = False
            if r == 0:
                jogou = True
                self.pos[self.id_quadrado][0][0] += self.size
            return self.pos, jogou
        return self.pos, False

    def cima(self):
        x, y = self.pos[self.id_quadrado][0]
        if y - self.size // 2 >= 0:
            r, g, b = self.rgb[x, y - self.size // 2]
            jogou = False
            if r == 0:
                jogou = True
                self.pos[self.id_quadrado][0][1] -= self.size
            return self.pos, jogou
        return self.pos, False

    def baixo(self):
        x, y = self.pos[self.id_quadrado][0]
        if y + self.size // 2 < self.img_height:
            r, g, b = self.rgb[x, y + self.size // 2]
            jogou = False
            if r == 0:
                jogou = True
                self.pos[self.id_quadrado][0][1] += self.size
            return self.pos, jogou
        return self.pos, False

    def draw_buttons(self):
        for i, (text, rect) in enumerate(self.buttons.items()):
            color = (0, 0, 0) if i != self.selected_button else (255, 0, 0)
            pygame.draw.rect(self.tela, color, rect)
            label = self.button_font.render(text, True, (255, 255, 255))
            self.tela.blit(label, (rect.x + 10, rect.y + 10))

    def start(self):
        self.fazer_caminho()

    def display(self):
        self.tela.fill((255, 255, 255))
        self.draw_buttons()
        pygame.display.flip()

    def check_move(self, direction):
        if direction == 'up':
            self.stack.append('up')
        elif direction == 'down':
            self.stack.append('down')
        elif direction == 'left':
            self.stack.append('left')
        elif direction == 'right':
            self.stack.append('right')
        elif direction == 'enter':
            self.process_movements()

    def process_movements(self):
        while self.stack:
            direction = self.stack.pop()
            if direction == "up":
                self.cima()
                print("cima")
            elif direction == "down":
                self.baixo()
                print('baixo')
            elif direction == "left":
                self.esquerda()
                print('esquerda')
            elif direction == "right":
                self.direita()
                print('direita')
            self.posicionar_jogadores(self.tela, self.pos, self.size)
            pygame.display.update()
            sleep(0.5)

    def run(self):
        pygame.init()
        self.start()
        while True:
            self.display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.check_move('up')
                    if event.key == pygame.K_DOWN:
                        self.check_move('down')
                    if event.key == pygame.K_LEFT:
                        self.check_move('left')
                    if event.key == pygame.K_RIGHT:
                        self.check_move('right')
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_button_click(event)
            pygame.display.update()