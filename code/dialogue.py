import pygame

class DialogBox:
    def __init__(self, display_surface, level):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, 36)
        self.is_active = False
        self.message = ""
        self.level = level
        self.dialogues = {
            'capecao_hub': [
                pygame.image.load('../graphics/dialogue/spr_dialoguebox_0.png'),
                pygame.image.load('../graphics/dialogue/mimir.png')
            ],
            'another_character': [
                pygame.image.load('../graphics/dialogue/AUAUAUAUAUAUAUUAUAUAUAUAUAU.png'),
                pygame.image.load('../graphics/dialogue/spr_dialoguebox_0.png'),
            ]
        }  # Dicionário com listas de imagens de diálogo
        self.current_dialogue = 'another_character'
        self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]  # Redimensiona as imagens se necessário
        self.current_image_index = 0

    def set_dialogue(self, dialogue_name):
        if dialogue_name in self.dialogues:
            self.current_dialogue = dialogue_name
            self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]
            self.current_image_index = 0

    def display(self, message):
        self.message = message
        self.is_active = True
        self._draw()

    def _draw(self):
        if self.is_active:
            overlay = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.display_surface.blit(overlay, (0, 0))

            message_surf = self.font.render(self.message, True, (255, 255, 255))
            message_rect = message_surf.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2))
            self.display_surface.blit(message_surf, message_rect)

            # Desenha a imagem do retângulo um pouco mais acima do centro inferior da tela
            rect_image_rect = self.rect_images[self.current_image_index].get_rect(midbottom=(self.display_surface.get_width() // 2, self.display_surface.get_height() - 50))
            self.display_surface.blit(self.rect_images[self.current_image_index], rect_image_rect)

    def check_trigger(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # Assumindo que a tecla 'F' é o gatilho
                self.is_active = not self.is_active
                self.level.show_dialogue = not self.level.show_dialogue
                self.level.toggle_menu()
                if self.is_active:
                    self.display("This is a dialog box")
            elif event.key == pygame.K_SPACE and self.is_active:  # Verifica se a barra de espaço foi pressionada
                self.current_image_index = (self.current_image_index + 1) % len(self.rect_images)  # Alterna para a próxima imagem
                self._draw()