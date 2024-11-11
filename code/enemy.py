import pygame
from support import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, pos,walls, attack_range=20, attack_damage=10):
        super().__init__()

        # Initialize the enemy's image and rect
        self.image = pygame.image.load('../graphics/monsters/raccoon/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Initialize graphics and animations
        self.import_enemy_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement and direction control
        self.direction = pygame.math.Vector2()
        self.player = player
        self.speed = 1
        self.position = pygame.math.Vector2(pos)

        # Attack parameters
        self.attack_range = attack_range
        self.attack_damage = attack_damage

        # Attack cooldown
        self.attack_cooldown = 1000
        self.last_attack_time = 0

        # Walls
        self.walls = walls

    def import_enemy_assets(self):
        enemy_path = '../graphics/monsters/raccoon/'
        self.animations = {'attack': [], 'idle': [], 'move': []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path)

    def attack_player(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            print(f"Enemy attacks the player! Damage: {self.attack_damage}")
            self.last_attack_time = current_time
            self.status = 'attack'

    def animate(self):
        animation = self.animations[self.status]
        if len(animation) == 0:
            return  # Ensure there are frames to animate

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_towards_player(self):
        player_position = pygame.math.Vector2(self.player.rect.center)
        distance_to_player = player_position - self.position

        if distance_to_player.length() <= self.attack_range:
            self.attack_player()
        else:
            direction = distance_to_player.normalize()
            self.position += direction * self.speed
            if abs(direction.x) > abs(direction.y):
                self.status = 'move' if direction.x > 0 else 'move'
            else:
                self.status = 'move' if direction.y > 0 else 'move'

            self.rect.topleft = self.position

    def check_collision(self):
        if self.rect.colliderect(self.player.rect):
            print("Player and enemy collided!")
            self.attack_player()

    def check_wall_collision(self):
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left
                if self.direction.x < 0:
                    self.rect.left = wall.rect.right
                if self.direction.y > 0:
                    self.rect.bottom = wall.rect.top
                if self.direction.y < 0:
                    self.rect.top = wall.rect.bottom

    def update(self):
        self.animate()
        self.move_towards_player()
        self.check_collision()
        self.check_wall_collision()