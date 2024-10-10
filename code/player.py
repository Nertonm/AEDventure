import pygame
from settings import *
from weapon import *
from capecao import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player/personagem1.png')
        self.rect = self.image.get_rect(topleft = (pos))
        self.hitbox = self.rect.inflate(0, -26)
        self.direction = pygame.math.Vector2()
        self.lado = ""
        self.speed = SPEED
        self.obstacle_sprites = obstacle_sprites
        self.sword = Sword(self)
        self.attacking = False
        self.cooldown = 500  # Tempo de espera  milissegundos
        self.attack_time = None  # Última vez que o jogador atacou
        self.capecao = Capecao(self)

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

    def cooldown_check(self):
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.cooldown:
                self.attacking = False


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.lado = "up"

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.lado = "down"

        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.lado = "right"

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.lado = "left"

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.attacking:  # Atacar com a tecla de espaço
            self.attack()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:    # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:    # moving left
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:    # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:    # moving top
                        self.hitbox.top = sprite.hitbox.bottom
                    
    def update(self):
        self.input()
        self.move(self.speed)
        self.sword.update()
        self.capecao.update()