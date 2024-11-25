import pygame
from settings import *
from debug import debug
from random import randint, randrange, shuffle
from time import sleep
from PIL import Image, ImageDraw


class MazeChallenge:

    def __init__(self, level, difficulty):
        # Usage at Level.__init__: self.challenge = MazeChallenge(self, self.difficulty)

        # Game settings
        self.level = level
        self.difficulty = difficulty
        self.is_active = True
        self.success = False  # == self.challenge_completed
        self.failure = False

        # Specific Settings
        if difficulty == 'easy':
            self.tamanho = [4, 4]
        elif difficulty == 'medium':
            self.tamanho = [6, 6]
        else:
            self.tamanho = [8, 8]
        # tamanho do espaço entre linhas
        self.size = 33
        self.maze = gerar_labirinto(self.tamanho[0], self.tamanho[1])
        img_new = Image.new('RGBA', (self.tamanho[0] * (self.size + 1) + 1, self.tamanho[1] * (self.size + 1) + 1), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.img_new)
        self.desenhar_labirinto_pillow()
        img_new.save("rect.png", "PNG")
        self.size += 1
        self.id_jogador = 0
        self.cor = [randint(15, 255), randint(15, 255), randint(15, 255)]

        # Graphics settings
        self.display_surface = pygame.display.get_surface()

        # UI
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.font_small = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.selected_button = None  # Adiciona o botão selecionado

        # Close Button
        button_width = 100
        button_height = 50
        self.close_button = pygame.Rect(
            (self.display_surface.get_width() - button_width) // 2,
            self.display_surface.get_height() - button_height - 10,
            button_width, button_height)

    @property
    def challenge_completed(self):
        return self.success

    @challenge_completed.setter
    def challenge_completed(self, value: bool):
        if type(value) == bool:
            self.success = value
        else:
            raise ValueError("challenge_completed must be boolean")

    # def generate_something(self): ...

    # def start(self): ...

    def toggle_menu(self):
        # Alterna o estado do menu de desafio
        self.is_active = not self.is_active
        if not self.is_active:
            self.level.reset_player_state()

    def input(self):
        # Gerencia a entrada do usuário

        keys = pygame.key.get_pressed()
        # current_time = pygame.time.get_ticks()
        # enter_cooldown = 200

        # Reinicia o do puzzle se o jogador falhar e pressionar Enter
        if self.failure:
            # if keys[pygame.K_RETURN] and current_time - self.last_enter_time >= enter_cooldown:
            if keys[pygame.K_RETURN]:
                self.failure = False
                self.is_active = True
                # Put here your Resetting Code
            return

        # Inativo ou completo
        if not self.is_active or self.success:
            return

        # Put here your specific input code
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self_selected_button = (self.selected_button - 1) % len(self.button_order)
                    if event.key == pygame.K_RIGHT:
                        self.selected_button = (self.selected_button + 1) % len(self.button_order)
                    if event.key == pygame.K_RETURN:
                        if self.button_order[self.selected_button] == "up":
                            self.movements_stack.append("up")
                        elif self.button_order[self.selected_button] == "down":
                            self.movements_stack.append("down")
                        elif self.button_order[self.selected_button] == "left":
                            self.movements_stack.append("left")
                        elif self.button_order[self.selected_button] == "right":
                            self.movements_stack.append("right")
                        elif self.button_order[self.selected_button] == "enter":
                            self.process_movements()
                self.check_button_click(event)


    def reset_with_failure(self):
        ...

    def is_solved(self):
        ...

        if ...:
            self.success = True
            self.level.mark_challenge_complete(self.__class__)
            self.challenge_completed = True

    def check_button_click(self, event):
        if not self.is_active:
            return
        # Verifica se o botão foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Botão de fechar
            if self.close_button.collidepoint(event.pos):
                if self.failure:
                    # Reinicia o estado do jogo se o jogador falhar e clicar em "Try Again"
                    self.failure = False
                    self.is_active = True
                    ...
                else:
                    self.is_active = False
                    self.level.reset_player_state()
                    # Garante que o menu de desafio não esteja ativo
                    self.level.show_challenge = False
                    # self.level.<nome do desafio>_challenge.is_active = False
                    self.success = False
                    self.failure = False
                    self.level.end_challenge()

            # Outros botões aqui!
            ...

    def check_button_hover(self):
        # Verifica se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        self.button_hovered = self.close_button.collidepoint(mouse_pos)

    def check_won(self, posicao, tamanho, size):
        for ID, p in posicao.items():
            if p[0] == [size / 2, tamanho[1] * size - size / 2]:
                return True

        return False

    def display(self):
        self.input()
        self.check_button_hover()

        surfaceSize=self.display_surface.get_size()
        surface = pygame.Surface(
            surfaceSize, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.display_surface.blit(surface, (0, 0))

        if not self.success and not self.failure:
            # Desenha o labirinto
            self.desenhar_labirinto_pillow()
            #codigo do jogo
            self.draw_buttons()

            vencedor = self.check_won(self.posicoes, self.tamanho, self.size)
            pygame.display.update()
            for pos in self.posicoes.values():
                x, y = pos[0]
                pygame.draw.rect(self.display_surface, pos[1], ((pos[0][0] - self.size / 2 + 1, pos[0][1] - self.size / 2 + 1), (self.size - 1, self.size - 1)))
            if vencedor:
                exit()
        # Close Button Render

        if self.failure:
            close_button_text = "Try Again"
            button_color = (
                0, 255, 0) if self.button_hovered or self.button_hovered else (255, 0, 0)
        else:
            close_button_text = "Close"
            button_color = (
                0, 255, 0) if self.button_hovered or self.button_hovered else (255, 0, 0)

        button_text_surf = self.font.render(
            close_button_text, True, (255, 255, 255))
        button_text_rect = button_text_surf.get_rect(
            center=self.close_button.center)
        self.close_button = button_text_rect
        pygame.draw.rect(self.display_surface,
                         button_color, self.close_button)
        self.display_surface.blit(button_text_surf, button_text_rect)

        # Success/Failure message

        if self.success:
            message_surf = self.font.render(
                "Congratulations!", True, (0, 255, 0))
            message_rect = message_surf.get_rect(
                center=self.display_surface.get_rect().center)
            self.display_surface.blit(message_surf, message_rect)
        elif self.failure:
            message_surf = self.font.render(
                "You fail!", True, (255, 0, 0))
            message_rect = message_surf.get_rect(
                center=self.display_surface.get_rect().center)
            self.display_surface.blit(message_surf, message_rect)

        # Exibe a mensagem se o desafio já foi completado
        if self.challenge_completed:
            completed_message = "You have completed this challenge."
            completed_message_surf = self.font_small.render(
                completed_message, True, (255, 255, 0))
            completed_message_rect = completed_message_surf.get_rect(
                center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 100))
            self.display_surface.blit(
                completed_message_surf, completed_message_rect)

        # debug(self.array, 500)
        pygame.display.update()
