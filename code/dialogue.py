import pygame
from settings import *

class DialogBox:
    def __init__(self, level):
        self.level = level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.dialogues = {
            'hub': [
                pygame.image.load('../graphics/dialogue/hub/dialogo_1.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_2.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_3.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_4.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_5.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_6.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_7.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_8.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_9.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_10.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_11.png'),
                pygame.image.load('../graphics/dialogue/hub/dialogo_12.png')
            ],
            'hanoi': [
                pygame.image.load('../graphics/dialogue/desafio hanoi/dialogo_0.png'),
                pygame.image.load('../graphics/dialogue/desafio hanoi/dialogo_1.png')
            ],
            'sorting': [
                pygame.image.load('../graphics/dialogue/desafio sorting/dialogo_0.png'),
                pygame.image.load('../graphics/dialogue/desafio sorting/dialogo_1.png')
            ],
            'room0': [
                pygame.image.load('../graphics/dialogue/desafio grafo/dialogo_0.png'),
                pygame.image.load('../graphics/dialogue/desafio grafo/dialogo_1.png')
            ],
            'meet': [
                pygame.image.load('../graphics/dialogue/meet/dialogo_0.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_1.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_2.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_3.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_4.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_5.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_6.png'),
                pygame.image.load('../graphics/dialogue/meet/dialogo_7.png')
            ],
            'start': [
                pygame.image.load('../graphics/dialogue/start/dialogo_0.png'),
                pygame.image.load('../graphics/dialogue/start/dialogo_1.png'),
                pygame.image.load('../graphics/dialogue/start/dialogo_2.png'),
                pygame.image.load('../graphics/dialogue/start/dialogo_3.png'),
                pygame.image.load('../graphics/dialogue/start/dialogo_4.png'),
                pygame.image.load('../graphics/dialogue/start/dialogo_5.png')
            ]
        }
        self.current_dialogue = 'start'
        self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]
        self.current_image_index = 0
        self.is_active = False
        self.selection_time = None
        self.can_move = True
        self.background_color = (0, 0, 0, 150)

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_SPACE] and self.is_active:
                self.current_image_index += 1
                if self.current_image_index >= len(self.rect_images):
                    self.is_active = False
                    self.level.show_dialogue = False
                    self.current_image_index = 0
                    self.level.resume_game()
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 200:
                self.can_move = True

    def set_dialogue(self, dialogue_name):
        if dialogue_name in self.dialogues:
            self.current_dialogue = dialogue_name
            self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]
            self.current_image_index = 0

    def _draw(self):
        if self.is_active:
            overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
            overlay.fill(self.background_color)
            self.display_surface.blit(overlay, (0, 0))

            rect_image_rect = self.rect_images[self.current_image_index].get_rect(
                midbottom=(self.display_surface.get_width() // 2, self.display_surface.get_height() - 50))
            self.display_surface.blit(self.rect_images[self.current_image_index], rect_image_rect)

    def toggle_dialogue(self):
        self.is_active = not self.is_active
        self.level.show_dialogue = not self.level.show_dialogue
        if self.is_active:
            self.display()
        else:
            self.level.toggle_menu()

    def display(self):
        self.input()
        self.selection_cooldown()

        self._draw()
        pygame.display.flip()