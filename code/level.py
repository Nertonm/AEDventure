import pygame
from settings import *
from tile import *
from player import Player
from debug import debug
from weapon import *
from capecao import *

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.ground_sprites = pygame.sprite.Group()  # Grupo só pro chão

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'd':
                    Door((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'x ':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'xd':
                    WallRight((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'xe':
                    WallLeft((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'xc':
                    WallUp((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'xb':
                    WallDown((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
                    self.capecao = Capecao(self.player)  # Cria a espada
                    self.visible_sprites.add(self.capecao)  # Adiciona a espada ao grupo visível

                    self.sword = Sword(self.player)  # Cria a espada
                    self.visible_sprites.add(self.sword)  # Adiciona a espada ao grupo visível
                    ground_sprite = Ground((x, y),[self.visible_sprites, self.ground_sprites])  # Adiciona ao ground_sprites
                    self.ground_sprites.add(ground_sprite)  # Adiciona explicitamente ao grupo de chão
                if col == ' ':
                    ground_sprite = Ground((x, y),[self.visible_sprites, self.ground_sprites])  # Adiciona ao ground_sprites
                    self.ground_sprites.add(ground_sprite)  # Adiciona explicitamente ao grupo de chão
                if col == 'rb':
                    RB((x,y),[self.visible_sprites,self.obstacle_sprites])


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Desenha primeiro os sprites de chão
        for ground_sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if isinstance(ground_sprite, Ground):  # Verifica se é um sprite de chão
                ground_offset_pos = ground_sprite.rect.topleft - self.offset
                self.display_surface.blit(ground_sprite.image, ground_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            if not isinstance(sprite, Ground): # Exclui sprites do chão
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)