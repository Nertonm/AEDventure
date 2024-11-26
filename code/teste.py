import pygame
import sys
import random
from jigsaw import Jigsaw
import settings

# Configuração inicial dos parâmetros de teste
settings.WIDTH = 800
settings.HEIGHT = 600
settings.UI_FONT = pygame.font.get_default_font()  # Substitua pelo caminho da fonte desejada, se necessário
settings.UI_FONT_SIZE_MENU = 30
GREY = (169, 169, 169)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)

def end_challenge_callback():
    print("Desafio concluído!")

def main():
    pygame.init()

    # Configuração da janela de exibição
    display_surface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Teste Jigsaw")

    # Inicializando o quebra-cabeça
    level = None  # Substitua isso pelo objeto de nível real, se necessário
    jigsaw = Jigsaw(level, display_surface, end_challenge_callback, 'easy')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                jigsaw.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = jigsaw.handle_mousebuttondown(event)

        # Atualizando a tela
        display_surface.fill(BLACK)
        jigsaw.draw_board()
        jigsaw.draw_close_button()
        pygame.display.flip()

        # Verificando se o quebra-cabeça foi concluído
        if jigsaw.check_won():
            running = False

        jigsaw.clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
