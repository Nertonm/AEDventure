import pygame
from support import import_folder

class Capecao(pygame.sprite.Sprite):
    def __init__(self, player, position):
        super().__init__()
        self.image = pygame.image.load('../graphics/capecao/right_idle/idle_right.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -26)
        self.attacking = False

        # graphics setup
        self.import_capecao_assets()
        self.status = 'right_idle'
        self.frame_index = 0
        self.animation_speed = 0.15

        # moviments
        self.direction = pygame.math.Vector2()
        self.player = player
        self.speed = 4
        self.position = position

    def import_capecao_assets(self):
        character_path = '../graphics/capecao/'
        self.animations = {'left': [], 'right': [], 'right_idle': [], 'left_idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
    
    def move(self):
        # IF trata do capecao seguindo o jogador pela direita
        # ELIF trata o capecao seguindo o jogador pela esquerda
        if self.rect.x < self.player.rect.x - 60:
            self.rect.x += self.speed
            self.status = 'right'
        elif self.rect.x > self.player.rect.x + 100:
            self.rect.x -= self.speed
            self.status = 'left'

        if self.rect.y < self.player.rect.y + 62:
            self.rect.y += self.speed
        elif self.rect.y > self.player.rect.y + 62:
            self.rect.y -= self.speed

    def update(self):
        self.animate()
        self.move()
        


