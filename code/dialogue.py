import pygame

class DialogBox:
    def __init__(self, display_surface, level):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, 36)
        self.is_active = False
        self.level = level
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
        }  # Dictionary with lists of dialogue images
        self.current_dialogue = 'start'
        self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]  # Resize images if necessary
        self.current_image_index = 0

    def set_dialogue(self, dialogue_name):
        if dialogue_name in self.dialogues:
            self.current_dialogue = dialogue_name
            self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]
            self.current_image_index = 0

    def display(self):
        self.is_active = True
        self._draw()

    def _draw(self):
        if self.is_active:
            overlay = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.display_surface.blit(overlay, (0, 0))

            # Desenha a imagem do retângulo um pouco mais acima do centro inferior da tela
            rect_image_rect = self.rect_images[self.current_image_index].get_rect(midbottom=(self.display_surface.get_width() // 2, self.display_surface.get_height() - 50))
            self.display_surface.blit(self.rect_images[self.current_image_index], rect_image_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Assumindo que a tecla 'F' é o gatilho
                self.toggle_dialogue()
            elif event.key == pygame.K_SPACE and self.is_active:  # Verifica se a barra de espaço foi pressionada
                self.current_image_index += 1
                if self.current_image_index >= len(self.rect_images):
                    self.is_active = False
                    self.level.show_dialogue = False
                    self.level.toggle_menu()
                    self.current_image_index = 0  # Reseta o índice de seleção
                else:
                    self._draw()

    def toggle_dialogue(self):
        self.is_active = not self.is_active
        self.level.show_dialogue = not self.level.show_dialogue
        self.level.toggle_menu()
        if self.is_active:
            self.display()