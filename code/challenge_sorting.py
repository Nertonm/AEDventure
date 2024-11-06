import pygame
import random
from settings import *

class SortingChallenge:
    def __init__(self, level):
        # Inicialização de variáveis e configuração inicial
        self.level = level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.font_small = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Fonte menor
        self.array = random.sample(range(1, 11), 10)
        self.selection_index = 0
        self.sorted = False
        self.cooldown = 200
        self.last_swap_time = 0
        self.can_swap = True
        self.move_cooldown_time = 200
        self.last_move_time = 0
        self.can_move = True
        self.is_active = True
        self.button_selected = False
        self.button_hovered = False
        self.enter_cooldown = 200  # Cooldown para a tecla Enter
        self.last_enter_time = 0
        self.challenge_completed = False  # Novo atributo

        # Configuração do botão de fechar
        button_width = 100
        button_height = 50
        self.button_rect = pygame.Rect(
            (self.display_surface.get_width() - button_width) // 2,
            self.display_surface.get_height() - button_height - 10,
            button_width,
            button_height
        )

        # Mensagens de sucesso e falha
        self.success_message = None
        self.failure_message = None

        # Gerar passos do Bubble Sort
        self.bubble_sort_steps = self.generate_bubble_sort_steps()
        self.current_step = 0

    def generate_bubble_sort_steps(self):
        # Gera os passos do algoritmo Bubble Sort
        steps = []
        arr = self.array[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    steps.append((j, j+1))
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return steps

    def toggle_menu(self):
        # Alterna o estado do menu de desafio
        self.is_active = not self.is_active
        if not self.is_active:
            self.level.reset_player_state()

    def input(self):
        # Gerencia a entrada do usuário
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.failure_message:
            if keys[pygame.K_RETURN] and current_time - self.last_enter_time >= self.enter_cooldown:
                # Reseta o estado do jogo se o jogador falhar e pressionar Enter
                self.array = random.sample(range(1, 11), 10)
                self.bubble_sort_steps = self.generate_bubble_sort_steps()
                self.current_step = 0
                self.failure_message = None
                self.is_active = True
                self.last_enter_time = current_time
                self.button_selected = False
            return

        if not self.is_active or self.success_message:
            return

        if self.can_move:
            if keys[pygame.K_LEFT] and not self.button_selected:
                self.selection_index -= 1
                if self.selection_index < 0:
                    self.selection_index = len(self.array) - 2
                self.can_move = False
                self.last_move_time = current_time
            elif keys[pygame.K_RIGHT] and not self.button_selected:
                self.selection_index += 1
                if self.selection_index >= len(self.array) - 1:
                    self.selection_index = 0
                self.can_move = False
                self.last_move_time = current_time
            elif keys[pygame.K_DOWN]:
                self.button_selected = True
                self.can_move = False
                self.last_move_time = current_time
            elif keys[pygame.K_UP] and self.button_selected:
                self.button_selected = False
                self.can_move = False
                self.last_move_time = current_time

        if keys[pygame.K_RETURN] and current_time - self.last_enter_time >= self.enter_cooldown:
            if self.button_selected:
                self.is_active = False
                self.level.reset_player_state()
                self.level.show_challenge = False  # Garante que o menu de desafio não esteja ativo
                self.level.sorting_challenge.is_active = False
                self.success_message = None
                self.failure_message = None
                self.level.end_challenge()
            else:
                self.swap_elements()
            self.last_enter_time = current_time

    def swap_elements(self):
        # Troca elementos do array
        if self.can_swap and not self.button_selected and not self.sorted:
            if self.selection_index < len(self.array) - 1:
                # Verifica se a troca do jogador corresponde ao passo do Bubble Sort
                expected_swap = self.bubble_sort_steps[self.current_step]
                if (self.selection_index, self.selection_index + 1) == expected_swap:
                    self.array[self.selection_index], self.array[self.selection_index + 1] = \
                        self.array[self.selection_index + 1], self.array[self.selection_index]
                    self.current_step += 1
                    self.check_sorted()
                else:
                    # Reinicia o array se a troca estiver incorreta e define a mensagem de falha
                    self.array = random.sample(range(1, 11), 10)
                    self.bubble_sort_steps = self.generate_bubble_sort_steps()
                    self.current_step = 0
                    self.failure_message = "You failed!"
                    self.button_selected = True

                self.can_swap = False
                self.last_swap_time = pygame.time.get_ticks()

    def swap_cooldown(self):
        # Gerencia o cooldown da troca de elementos
        if not self.can_swap:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_swap_time >= self.cooldown:
                self.can_swap = True

    def move_cooldown(self):
        # Gerencia o cooldown do movimento
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time >= self.move_cooldown_time:
                self.can_move = True

    def check_sorted(self):
        self.sorted = all(self.array[i] <= self.array[i + 1] for i in range(len(self.array) - 1))
        if self.sorted:
            self.success_message = "Congratulations!"
            self.level.mark_challenge_complete()
            self.challenge_completed = True  # Desafio completado

    def check_button_click(self, event):
        if not self.is_active:
            return
        # Verifica se o botão foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                if self.failure_message:
                    # Reseta o estado do jogo se o jogador falhar e clicar em "Try Again"
                    self.array = random.sample(range(1, 11), 10)
                    self.bubble_sort_steps = self.generate_bubble_sort_steps()
                    self.current_step = 0
                    self.failure_message = None
                    self.is_active = True
                else:
                    self.is_active = False
                    self.level.reset_player_state()
                    self.level.show_challenge = False  # Garante que o menu de desafio não esteja ativo
                    self.level.sorting_challenge.is_active = False
                    self.success_message = None
                    self.failure_message = None
                    self.level.end_challenge()

    def check_button_hover(self):
        # Verifica se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        self.button_hovered = self.button_rect.collidepoint(mouse_pos)

    def display(self):
        if not self.is_active:
            return

        self.input()
        self.swap_cooldown()
        self.move_cooldown()
        self.check_button_hover()

        surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.display_surface.blit(surface, (0, 0))

        if not self.success_message and not self.failure_message:
            total_width = len(self.array) * 100
            start_x = (self.display_surface.get_width() - total_width) // 2

            if self.selection_index < len(self.array) - 1:
                swap_rect_x = start_x + self.selection_index * 100
                swap_rect_width = 200
                swap_rect = pygame.Rect(swap_rect_x, self.display_surface.get_height() // 2 - 50, swap_rect_width, 100)
                swap_surface = pygame.Surface((swap_rect.width, swap_rect.height), pygame.SRCALPHA)
                swap_surface.fill((200, 200, 200, 150))
                self.display_surface.blit(swap_surface, (swap_rect.x, swap_rect.y))

            for index, value in enumerate(self.array):
                if index == self.selection_index:
                    color = TEXT_COLOR_SELECTED
                elif index == self.selection_index + 1:
                    color = TEXT_COLOR_SECOND_SELECTED
                else:
                    color = TEXT_COLOR
                value_surf = self.font.render(str(value), True, color)
                value_rect = value_surf.get_rect(
                    center=(start_x + index * 100 + 50, self.display_surface.get_height() // 2))
                self.display_surface.blit(value_surf, value_rect)

        if self.failure_message:
            button_text = "Try Again"
            button_color = (0, 255, 0) if self.button_hovered or self.button_selected else (255, 0, 0)
        else:
            button_text = "Close"
            button_color = (0, 255, 0) if self.button_hovered or self.button_selected else (255, 0, 0)

        button_text_surf = self.font.render(button_text, True, (255, 255, 255))
        button_text_rect = button_text_surf.get_rect(center=self.button_rect.center)
        self.button_rect = button_text_rect
        pygame.draw.rect(self.display_surface, button_color, self.button_rect)
        self.display_surface.blit(button_text_surf, button_text_rect)

        if self.success_message:
            message_surf = self.font.render(self.success_message, True, (0, 255, 0))
            message_rect = message_surf.get_rect(center=self.display_surface.get_rect().center)
            self.display_surface.blit(message_surf, message_rect)
        elif self.failure_message:
            message_surf = self.font.render(self.failure_message, True, (255, 0, 0))
            message_rect = message_surf.get_rect(center=self.display_surface.get_rect().center)
            self.display_surface.blit(message_surf, message_rect)

        # Exibe a mensagem se o desafio já foi completado
        if self.challenge_completed:
            completed_message = "You have completed this challenge."
            completed_message_surf = self.font_small.render(completed_message, True, (255, 255, 0))
            completed_message_rect = completed_message_surf.get_rect(
                center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 100))
            self.display_surface.blit(completed_message_surf, completed_message_rect)

        pygame.display.update()
