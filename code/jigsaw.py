import pygame
import sys
import random
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN


class Button:
    def __init__(self, text, pos, size, font, color, text_color, action=None):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action
        self.rect = pygame.Rect(pos, size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # Borda do botão
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Jigsaw:
    def __init__(self, vh_num, display_surface):
        self.vh_num = vh_num
        self.cell_num = vh_num * vh_num
        self.board = list(range(self.cell_num))
        self.display_surface = display_surface
        self.image = pygame.image.load(f"00{vh_num}.png")
        self.rect = self.image.get_rect()
        self.cell_width = self.rect.width // vh_num
        self.cell_height = self.rect.height // vh_num
        self.shuffle_board()

    def shuffle_board(self):
        while True:
            random.shuffle(self.board)
            self.white_cell = self.board.index(self.cell_num - 1)
            if self.is_resolvable():
                break

    def is_resolvable(self):
        inversions = self.count_inversions()
        white_distance = (self.vh_num - 1) - self.white_cell // self.vh_num
        if self.vh_num % 2 != 0:
            return inversions % 2 == 0
        return (inversions % 2 == 0) == (white_distance % 2 == 0)

    def count_inversions(self):
        inversions = 0
        temp = [self.board[i] for i in range(self.cell_num) if i != self.white_cell]
        for i in range(len(temp)):
            for j in range(i + 1, len(temp)):
                if temp[i] > temp[j]:
                    inversions += 1
        return inversions

    def is_finished(self):
        return all(i == self.board[i] for i in range(self.cell_num))

    def draw_board(self):
        for i in range(self.cell_num):
            row_dst = i // self.vh_num
            col_dst = i % self.vh_num
            rect_dst = pygame.Rect(col_dst * self.cell_width, row_dst * self.cell_height, self.cell_width, self.cell_height)

            if i != self.white_cell:
                row_src = self.board[i] // self.vh_num
                col_src = self.board[i] % self.vh_num
                rect_src = pygame.Rect(col_src * self.cell_width, row_src * self.cell_height, self.cell_width, self.cell_height)
                self.display_surface.blit(self.image, rect_dst, rect_src)

        self.draw_grid()

    def draw_grid(self):
        for i in range(self.vh_num):
            pygame.draw.line(self.display_surface, (0, 0, 0), (0, i * self.cell_height), (self.rect.width, i * self.cell_height))
            pygame.draw.line(self.display_surface, (0, 0, 0), (i * self.cell_width, 0), (i * self.cell_width, self.rect.height))

    def handle_mouse_event(self, pos):
        x, y = pos
        row = y // self.cell_height
        col = x // self.cell_width
        index = row * self.vh_num + col

        if self.is_valid_move(index):
            self.board[index], self.board[self.white_cell] = self.board[self.white_cell], self.board[index]
            self.white_cell = index

    def is_valid_move(self, index):
        return (
            index == self.white_cell - self.vh_num or
            index == self.white_cell + self.vh_num or
            (self.white_cell % self.vh_num != self.vh_num - 1 and index == self.white_cell + 1) or
            (self.white_cell % self.vh_num != 0 and index == self.white_cell - 1)
        )


def run_game(vh_num):
    pygame.init()
    screen = pygame.display.set_mode((600, 650))  # Aumentado para acomodar o botão
    pygame.display.set_caption(f"{vh_num}x{vh_num} Jigsaw Puzzle")
    font = pygame.font.Font(None, 40)

    game = Jigsaw(vh_num, screen)

    button = Button(
        text="Reiniciar",
        pos=(225, 600),  # Canto inferior central
        size=(150, 40),
        font=font,
        color=(200, 200, 200),
        text_color=(0, 0, 0),
        action=lambda: game.shuffle_board()  # Reinicia o jogo
    )

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if button.is_clicked(event.pos):
                    button.action()
                else:
                    game.handle_mouse_event(event.pos)

        screen.fill((255, 255, 255))
        game.draw_board()
        button.draw(screen)
        pygame.display.flip()

        if game.is_finished():
            print("Você venceu!")
            return


run_game(3)
