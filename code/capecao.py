import pygame

class Capecao(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('../pseucapecao1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.attacking = False
        self.player = player

    def update(self):
        # Posiciona o Capecão no lado oposto ao que o jogador está olhando
        if self.player.lado == "right":
            self.rect.midright = self.player.rect.midleft  # Capecão à esquerda
        elif self.player.lado == "left":
            self.rect.midleft = self.player.rect.midright  # Capecão à direita
        elif self.player.lado == "up":
            self.rect.midtop = self.player.rect.midbottom  # Capecão abaixo
        elif self.player.lado == "down":
            self.rect.midbottom = self.player.rect.midtop  # Capecão acima


