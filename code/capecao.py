import pygame

class Capecao(pygame.sprite.Sprite):
    def __init__(self, player, position):
        super().__init__()
        self.image = pygame.image.load('../graphics/capecao/right_idle/idle_right.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.attacking = False
        self.player = player
        self.speed = 4
        self.position = position
    
    def update(self):
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < self.player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > self.player.rect.y:
            self.rect.y -= self.speed
    
        


