import pygame
import random
from settings import *
from debug import debug

class SortingChallenge:
    def __init__(self, level, difficulty):
        # Inicialização de variáveis e configuração inicial
        self.level = level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.font_small = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.difficulty = None  # Adiciona a dificuldade como None inicialmente
        self.selected_button = None  # Adiciona o botão selecionado
        self.array = []
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
        self.enter_cooldown = 200
        self.last_enter_time = 0
        self.challenge_completed = False
        self.sort_algorithm = None
        self.current_position = 0
        # Adiciona a dificuldade
        self.difficulty = difficulty

        # Configuração dos botões de seleção de algoritmo
        self.bubble_button_rect = pygame.Rect(
            (self.display_surface.get_width() // 2) - 150,
            self.display_surface.get_height() // 2,
            100,
            50
        )
        self.selection_button_rect = pygame.Rect(
            (self.display_surface.get_width() // 2) + 50,
            self.display_surface.get_height() // 2,
            100,
            50
        )
        self.hard_button_rect = pygame.Rect(  # Adiciona a definição do hard_button_rect
            (self.display_surface.get_width() // 2) + 200,
            self.display_surface.get_height() // 2,
            100,
            50
        )

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

        # Gerar passos do algoritmo de ordenação
        self.sort_steps = []
        self.current_step = 0

    def generate_sort_steps(self):
        if self.sort_algorithm == 'bubble':
            return self.generate_bubble_sort_steps()
        elif self.sort_algorithm == 'selection':
            return self.generate_selection_sort_steps()

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

    def generate_selection_sort_steps(self):
        # Gera os passos do algoritmo Selection Sort
        steps = []
        arr = self.array[:]
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                steps.append((i, min_idx))
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return steps

    def select_sort_algorithm(self, algorithm):
        # Permite ao jogador selecionar o algoritmo de ordenação
        if algorithm in ['bubble', 'selection']:
            self.sort_algorithm = algorithm
            self.array = self.generate_array()  # Gera o array com base na dificuldade
            self.sort_steps = self.generate_sort_steps()
            self.current_step = 0
            self.sorted = False
            self.success_message = None
            self.failure_message = None
            self.current_position = 0  # Resetar a posição inicial para o Selection Sort

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
                self.array = self.generate_array()
                self.sort_steps = self.generate_sort_steps()
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
                if self.sort_algorithm == 'bubble':
                    if self.selection_index < 0:
                        self.selection_index = len(self.array) - 2
                else:
                    if self.selection_index < 0:
                        self.selection_index = len(self.array) - 1
                self.can_move = False
                self.last_move_time = current_time
            elif keys[pygame.K_RIGHT] and not self.button_selected:
                self.selection_index += 1
                if self.sort_algorithm == 'bubble':
                    if self.selection_index >= len(self.array) - 1:
                        self.selection_index = 0
                else:
                    if self.selection_index >= len(self.array):
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
            if self.sort_algorithm == 'bubble':
                if self.selection_index < len(self.array) - 1:
                    expected_swap = self.sort_steps[self.current_step]
                    if (self.selection_index, self.selection_index + 1) == expected_swap:
                        self.array[self.selection_index], self.array[self.selection_index + 1] = \
                            self.array[self.selection_index + 1], self.array[self.selection_index]
                        self.current_step += 1
                        self.check_sorted()
                    else:
                        self.reset_array_with_failure()
            elif self.sort_algorithm == 'selection':
                if self.selection_index < len(self.array):
                    min_index = self.find_min_index(self.current_position)
                    if self.selection_index == min_index:
                        self.array[self.current_position], self.array[min_index] = \
                            self.array[min_index], self.array[self.current_position]
                        self.current_position += 1
                        self.current_step += 1
                        self.check_sorted()
                    else:
                        self.reset_array_with_failure()

            self.can_swap = False
            self.last_swap_time = pygame.time.get_ticks()

    def find_min_index(self, start):
        # Encontra o índice do menor elemento no subarray não ordenado
        min_idx = start
        for i in range(start + 1, len(self.array)):
            if self.array[i] < self.array[min_idx]:
                min_idx = i
        return min_idx

    def reset_array_with_failure(self):
        # Reinicia o array se a troca estiver incorreta e define a mensagem de falha
        self.array = self.generate_array()  # Gera o array com base na dificuldade
        self.sort_steps = self.generate_sort_steps()
        self.current_step = 0
        self.current_position = 0
        self.failure_message = "You failed!"
        self.button_selected = True

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
                    self.array = self.generate_array()
                    self.sort_steps = self.generate_sort_steps()
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
            elif self.sort_algorithm is None:  # Verifica se o algoritmo já foi selecionado
                if self.bubble_button_rect.collidepoint(event.pos):
                    self.select_sort_algorithm('bubble')
                elif self.selection_button_rect.collidepoint(event.pos):
                    self.select_sort_algorithm('selection')

    def check_button_hover(self):
        # Verifica se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        self.button_hovered = self.button_rect.collidepoint(mouse_pos)

    def display(self):
        if not self.is_active:
            self.display_difficulty_selection()
            return

        self.input()
        self.swap_cooldown()
        self.move_cooldown()
        self.check_button_hover()

        surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.display_surface.blit(surface, (0, 0))

        if self.sort_algorithm is None:
            # Exibe a tela de seleção do algoritmo
            self.display_algorithm_selection()
        else:
            if not self.success_message and not self.failure_message:
                total_width = len(self.array) * 120  # Aumenta o espaço total
                start_x = (self.display_surface.get_width() - total_width) // 2

                if self.sort_algorithm == 'bubble':
                    if self.selection_index < len(self.array) - 1:
                        swap_rect_x = start_x + self.selection_index * 120
                        swap_rect_width = 240
                        swap_rect = pygame.Rect(swap_rect_x, self.display_surface.get_height() // 2 - 50,
                                                swap_rect_width, 100)
                        swap_surface = pygame.Surface((swap_rect.width, swap_rect.height), pygame.SRCALPHA)
                        swap_surface.fill((200, 200, 200, 150))
                        self.display_surface.blit(swap_surface, (swap_rect.x, swap_rect.y))
                elif self.sort_algorithm == 'selection':
                    if self.selection_index < len(self.array):
                        swap_rect_x = start_x + self.selection_index * 120
                        swap_rect_width = 120
                        swap_rect = pygame.Rect(swap_rect_x, self.display_surface.get_height() // 2 - 50,
                                                swap_rect_width, 100)
                        swap_surface = pygame.Surface((swap_rect.width, swap_rect.height), pygame.SRCALPHA)
                        swap_surface.fill((200, 200, 200, 150))
                        self.display_surface.blit(swap_surface, (swap_rect.x, swap_rect.y))

                for index, value in enumerate(self.array):
                    if self.sort_algorithm == 'bubble':
                        if index == self.selection_index:
                            color = TEXT_COLOR_SELECTED
                        elif index == self.selection_index + 1:
                            color = TEXT_COLOR_SECOND_SELECTED
                        else:
                            color = TEXT_COLOR
                    elif self.sort_algorithm == 'selection':
                        if index == self.selection_index:
                            color = TEXT_COLOR_SELECTED
                        elif index == self.current_position:
                            color = TEXT_COLOR_SECOND_SELECTED
                        else:
                            color = TEXT_COLOR
                    value_surf = self.font_small.render(str(value), True, color)
                    value_rect = value_surf.get_rect(
                        center=(start_x + index * 120 + 60, self.display_surface.get_height() // 2))
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

        debug(self.array, 500)
        pygame.display.update()

    def display_algorithm_selection(self):
        # Exibe a tela de seleção do algoritmo
        selection_message = "Escolha o tipo de algoritmo de ordenacao"
        selection_message_surf = self.font_small.render(selection_message, True, (255, 255, 255))
        selection_message_rect = selection_message_surf.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 100))
        self.display_surface.blit(selection_message_surf, selection_message_rect)

        # Ajusta a posição dos botões para aumentar a distância entre eles
        bubble_button_text = "Bubble Sort"
        bubble_button_color = (0, 255, 0) if self.bubble_button_rect.collidepoint(pygame.mouse.get_pos()) else (
        255, 0, 0)
        bubble_button_surf = self.font_small.render(bubble_button_text, True, (255, 255, 255))
        bubble_button_rect = bubble_button_surf.get_rect(
            center=(self.display_surface.get_width() // 2 - 200, self.display_surface.get_height() // 2))
        bubble_button_rect.inflate_ip(20, 10)  # Aumenta o tamanho do retângulo
        self.bubble_button_rect = bubble_button_rect  # Atualiza a área de colisão
        pygame.draw.rect(self.display_surface, bubble_button_color, bubble_button_rect)
        bubble_button_surf_rect = bubble_button_surf.get_rect(center=bubble_button_rect.center)
        self.display_surface.blit(bubble_button_surf, bubble_button_surf_rect)

        selection_button_text = "Selection Sort"
        selection_button_color = (0, 255, 0) if self.selection_button_rect.collidepoint(pygame.mouse.get_pos()) else (
        255, 0, 0)
        selection_button_surf = self.font_small.render(selection_button_text, True, (255, 255, 255))
        selection_button_rect = selection_button_surf.get_rect(
            center=(self.display_surface.get_width() // 2 + 200, self.display_surface.get_height() // 2))
        selection_button_rect.inflate_ip(20, 10)  # Aumenta o tamanho do retângulo
        self.selection_button_rect = selection_button_rect  # Atualiza a área de colisão
        pygame.draw.rect(self.display_surface, selection_button_color, selection_button_rect)
        selection_button_surf_rect = selection_button_surf.get_rect(center=selection_button_rect.center)
        self.display_surface.blit(selection_button_surf, selection_button_surf_rect)

    def display_difficulty_selection(self):
        # Exibe a tela de seleção de dificuldade
        selection_message = "Escolha a dificuldade"
        selection_message_surf = self.font_small.render(selection_message, True, (255, 255, 255))
        selection_message_rect = selection_message_surf.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 100))

        # Cria uma superfície semi-transparente
        overlay = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
        overlay.set_alpha(128)  # Define a transparência (0-255)
        overlay.fill((0, 0, 0))  # Preenche a superfície com a cor preta
        self.display_surface.blit(overlay, (0, 0))  # Desenha a superfície na tela

        self.display_surface.blit(selection_message_surf, selection_message_rect)

        mouse_pos = pygame.mouse.get_pos()

        easy_button_text = "Easy"
        easy_button_color = (0, 255, 0) if self.bubble_button_rect.collidepoint(mouse_pos) else (255, 0, 0)
        easy_button_surf = self.font_small.render(easy_button_text, True, (255, 255, 255))
        easy_button_rect = easy_button_surf.get_rect(
            center=(self.display_surface.get_width() // 2 - 200, self.display_surface.get_height() // 2))
        easy_button_rect.inflate_ip(20, 10)
        self.bubble_button_rect = easy_button_rect
        pygame.draw.rect(self.display_surface, easy_button_color, easy_button_rect)
        easy_button_surf_rect = easy_button_surf.get_rect(center=easy_button_rect.center)
        self.display_surface.blit(easy_button_surf, easy_button_surf_rect)

        medium_button_text = "Normal"
        medium_button_color = (0, 255, 0) if self.selection_button_rect.collidepoint(mouse_pos) else (255, 0, 0)
        medium_button_surf = self.font_small.render(medium_button_text, True, (255, 255, 255))
        medium_button_rect = medium_button_surf.get_rect(
            center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
        medium_button_rect.inflate_ip(20, 10)
        self.selection_button_rect = medium_button_rect
        pygame.draw.rect(self.display_surface, medium_button_color, medium_button_rect)
        medium_button_surf_rect = medium_button_surf.get_rect(center=medium_button_rect.center)
        self.display_surface.blit(medium_button_surf, medium_button_surf_rect)

        hard_button_text = "Hard"
        hard_button_color = (0, 255, 0) if self.hard_button_rect.collidepoint(mouse_pos) else (255, 0, 0)
        hard_button_surf = self.font_small.render(hard_button_text, True, (255, 255, 255))
        hard_button_rect = hard_button_surf.get_rect(
            center=(self.display_surface.get_width() // 2 + 200, self.display_surface.get_height() // 2))
        hard_button_rect.inflate_ip(20, 10)
        self.hard_button_rect = hard_button_rect
        pygame.draw.rect(self.display_surface, hard_button_color, hard_button_rect)
        hard_button_surf_rect = hard_button_surf.get_rect(center=hard_button_rect.center)
        self.display_surface.blit(hard_button_surf, hard_button_surf_rect)

    def generate_array(self):
        # Gera o array com base na dificuldade
        if self.difficulty == 'easy':
            return random.sample(range(1, 11), 10)
        elif self.difficulty == 'hard':
            return random.sample(range(1, 201), 10)
        else:  # medium
            return random.sample(range(1, 101), 10)

    def check_difficulty_selection(self, event):
        # Verifica se o jogador selecionou uma dificuldade
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.bubble_button_rect.collidepoint(event.pos):
                self.difficulty = 'easy'
                self.selected_button = 'easy'
            elif self.selection_button_rect.collidepoint(event.pos):
                self.difficulty = 'medium'
                self.selected_button = 'medium'
            elif self.hard_button_rect.collidepoint(event.pos):
                self.difficulty = 'hard'
                self.selected_button = 'hard'
            if self.difficulty:
                self.is_active = True

