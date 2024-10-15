import pygame
import sys
from settings import *
from level import Level
from support import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('AEDventure')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.menu = Menu()
        self.menu.load_button_images()

        self.resume_button = self.menu.resume_button
        self.options_button = self.menu.options_button
        self.quit_button = self.menu.quit_button
        self.video_button = self.menu.video_button
        self.audio_button = self.menu.audio_button
        self.keys_button = self.menu.keys_button
        self.back_button = self.menu.back_button

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def run(self):
        font = pygame.font.SysFont("Comic Sans", 40)
        game_paused = True
        menu_state = "main"
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Cor de Fundo
            self.screen.fill((66, 66, 66))

            if game_paused:
                keys = pygame.key.get_pressed()
                if menu_state == "main":
                    # Desenhar botões da tela de pausa
                    if self.resume_button.draw(self.screen) or keys[pygame.K_ESCAPE]:
                        del keys
                        game_paused = False
                    self.draw_text("Resume", font, TEXT_COLOR, 374, 135)
                    if self.options_button.draw(self.screen):
                        menu_state = "options"
                    self.draw_text("Options", font, TEXT_COLOR, 367, 260)
                    if self.quit_button.draw(self.screen):
                        run = False
                    self.draw_text("Quit", font, TEXT_COLOR, 406, 385)

                elif menu_state == "options":
                    # Desenhar os botões de opções
                    if self.video_button.draw(self.screen):
                        print("Video Settings")
                    self.draw_text("Video Settings", font, TEXT_COLOR, 150, 150)
                    if self.audio_button.draw(self.screen):
                        print("Audio Settings")
                    self.draw_text("Audio Settings", font, TEXT_COLOR, 150, 200)
                    if self.keys_button.draw(self.screen):
                        print("Change Key Bindings")
                    self.draw_text("Change Key Bindings", font, TEXT_COLOR, 150, 250)
                    if self.back_button.draw(self.screen):
                        menu_state = "main"
                    self.draw_text("Back", font, TEXT_COLOR, 150, 300)

            else:
                self.draw_text("Press P to pause", font, TEXT_COLOR, 150, 250)
                self.level.run()

            # Tratamento de eventos
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                game_paused = True
                del keys

            pygame.display.update()
            self.clock.tick(60)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
