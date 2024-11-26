import pygame
import random
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width - 60, 10)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

        # walking sounds
        self.walking_sounds = [pygame.mixer.Sound(f'../audio/sfx/walk/Steps_tiles-{i}.ogg') for i in range(1, 10)]
        for sound in self.walking_sounds:
            sound.set_volume(0.085)  # Adjust the volume of walking sounds
        self.is_walking = False
        self.walk_sound_timer = 0
        self.walk_sound_delay = 275  # Delay in milliseconds between each step sound
        self.running = False

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        # movement input
        if keys[MOVE_UP] or keys[MOVE_UP1]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[MOVE_DOWN] or keys[MOVE_DOWN1]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[MOVE_RIGHT] or keys[MOVE_RIGHT1]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[MOVE_LEFT] or keys[MOVE_LEFT1]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        # check if running
        self.running = keys[SPRINT] or keys[SPRINT1]

        # play walking sound
        if self.direction.x != 0 or self.direction.y != 0:
            if not self.is_walking:
                self.is_walking = True
                self.walk_sound_timer = pygame.time.get_ticks()  # Reset the timer
                self.play_walk_sound()
        else:
            if self.is_walking:
                self.is_walking = False
                self.stop_walk_sound()

    def play_walk_sound(self):
        if self.is_walking:
            current_time = pygame.time.get_ticks()
            delay = self.walk_sound_delay // 2 if self.running else self.walk_sound_delay
            if current_time - self.walk_sound_timer >= delay:
                self.walk_sound_timer = current_time
                sound = random.choice(self.walking_sounds)
                sound.play()

    def stop_walk_sound(self):
        for sound in self.walking_sounds:
            sound.stop()

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status:
                self.status = self.status + '_idle'

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        if self.running:
            speed *= 2
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.collidepoint(self.hitbox.midright) and self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                if sprite.hitbox.collidepoint(self.hitbox.midleft) and self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.collidepoint(self.hitbox.midbottom) and self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                if sprite.hitbox.collidepoint(self.hitbox.midtop) and self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Player death logic
        print("Player died!")

    def update(self):
        self.input()
        self.play_walk_sound()  # Ensure the sound plays continuously
        self.get_status()
        self.animate()
        self.move(self.speed)