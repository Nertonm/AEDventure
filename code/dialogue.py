import pygame, sys, time
import settings

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
        }
        self.current_dialogue = 'start'
        self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]
        self.current_image_index = 0
        self.clock = pygame.time.Clock()

    def set_dialogue(self, dialogue_name):
        if dialogue_name in self.dialogues:
            self.current_dialogue = dialogue_name
            self.rect_images = [pygame.transform.scale(img, (960, 192)) for img in self.dialogues[self.current_dialogue]]
            self.current_image_index = 0

    def _draw(self):
        if self.is_active:
            # Desenha a superfície transparente preta
            overlay = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Define a transparência
            self.display_surface.blit(overlay, (0, 0))

            # Desenha a imagem do diálogo
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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.toggle_dialogue()
                    if event.key == pygame.K_SPACE and self.is_active:
                        self.current_image_index += 1
                        if self.current_image_index >= len(self.rect_images):
                            self.is_active = False
                            self.level.show_dialogue = False
                            self.current_image_index = 0
                            self.level.resume_game()
                            running = False
                        else:
                            self._draw()

            self.level.run()  # Desenha a superfície original do level
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)