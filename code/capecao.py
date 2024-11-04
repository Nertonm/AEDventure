import pygame

class Capecao(pygame.sprite.Sprite):
    def __init__(self, player, position):
        super().__init__()
        self.image = pygame.image.load('../graphics/capecao/right_idle/idle_right.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.attacking = False
        self.player = player
        self.speed = 3
    
    def update(self):
        player_pos = self.player.rect.center
        capecao_pos = position
        direction = pygame.math.Vector2(player_pos) - pygame.math.Vector2(capecao_pos)

        if direction.length() > 1:
            direction = direction.normalize()  # Normaliza a direção

        # o capecão vai ser atraído de acordo com o movimento do jogador
        self.rect.centerx += direction.x * self.speed
        self.rect.centery += direction.y * self.speed
    
        


