import pygame
import random
from settings import *

class SortingChallenge:
    def __init__(self, level):
        self.level = level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
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

        button_width = 100
        button_height = 50
        self.button_rect = pygame.Rect(
            (self.display_surface.get_width() - button_width) // 2,
            self.display_surface.get_height() - button_height - 10,
            button_width,
            button_height
        )

    def toggle_menu(self):
        self.is_active = not self.is_active
        if not self.is_active:
            self.level.reset_player_state()

    def input(self):
        if not self.is_active:
            return

        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_LEFT] and not self.button_selected:
                self.selection_index -= 1
                if self.selection_index < 0:
                    self.selection_index = len(self.array) - 1
                self.can_move = False
                self.last_move_time = pygame.time.get_ticks()
            elif keys[pygame.K_RIGHT] and not self.button_selected:
                self.selection_index += 1
                if self.selection_index >= len(self.array):
                    self.selection_index = 0
                self.can_move = False
                self.last_move_time = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN]:
                self.button_selected = True
                self.can_move = False
                self.last_move_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.button_selected:
                self.button_selected = False
                self.can_move = False
                self.last_move_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if self.button_selected:
                self.is_active = False
                self.level.reset_player_state()
            else:
                self.swap_elements()

    def swap_elements(self):
        if self.can_swap and not self.button_selected:
            if self.selection_index < len(self.array) - 1:
                self.array[self.selection_index], self.array[self.selection_index + 1] = \
                    self.array[self.selection_index + 1], self.array[self.selection_index]
                self.check_sorted()
                self.can_swap = False
                self.last_swap_time = pygame.time.get_ticks()

    def swap_cooldown(self):
        if not self.can_swap:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_swap_time >= self.cooldown:
                self.can_swap = True

    def move_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time >= self.move_cooldown_time:
                self.can_move = True

    def check_sorted(self):
        self.sorted = all(self.array[i] <= self.array[i + 1] for i in range(len(self.array) - 1))
        if self.sorted:
            self.level.complete_challenge()
            self.is_active = False

    def check_button_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.is_active = False
                self.level.reset_player_state()

    def check_button_hover(self):
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

        total_width = len(self.array) * 100
        start_x = (self.display_surface.get_width() - total_width) // 2

        for index, value in enumerate(self.array):
            color = TEXT_COLOR_SELECTED if index == self.selection_index and not self.button_selected else TEXT_COLOR
            value_surf = self.font.render(str(value), True, color)
            value_rect = value_surf.get_rect(
                center=(start_x + index * 100 + 50, self.display_surface.get_height() // 2))
            self.display_surface.blit(value_surf, value_rect)

        button_color = (0, 255, 0) if self.button_hovered or self.button_selected else (255, 0, 0)
        pygame.draw.rect(self.display_surface, button_color, self.button_rect)
        button_text = self.font.render("Close", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.display_surface.blit(button_text, button_text_rect)

        pygame.display.update()