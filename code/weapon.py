import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('../graphics/weapons/sword/full.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.attacking = False
        self.player = player

    def update(self):
        # Atualiza a posição da espada baseada na posição do jogador
        if self.player.lado == "right":
            self.rect.midleft = self.player.rect.midright  # Posiciona à direita
        elif self.player.lado == "left":
            self.rect.midright = self.player.rect.midleft  # Posiciona à esquerda
        elif self.player.lado == "up":
            self.rect.midbottom = self.player.rect.midtop  # Posiciona acima
        elif self.player.lado == "down":
            self.rect.midtop = self.player.rect.midbottom  # Posiciona abaixo

