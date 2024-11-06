import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from menu import Menu
from challenge_sorting import SortingChallenge
import pytmx
from capecao import *
import random
from collections import deque

class Level:
    def __init__(self):
        # Inicialização de variáveis e grupos de sprites
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        # Carregamento do mapa e dados do TMX
        self.create_map('../map/map.tmx')
        self.tmx_data = pytmx.load_pygame('../map/map.tmx')

        # Inicialização de menus e desafios
        self.pause_menu = Menu(self)
        self.challenge = None
        self.menu = Menu(self)
        self.sorting_challenge = SortingChallenge(self)

        # Estados do jogo
        self.show_menu = False
        self.show_challenge = False
        self.player_can_move = True

    def get_pos(self, tmx_data, name):
        # Obtém a posição de um objeto no mapa pelo nome
        for obj in tmx_data.objects:
            if obj.name == name:
                return obj.x, obj.y
        return 0, 0

    def get_name(self, tmx_data, pos):
        # Obtém o nome de um objeto no mapa pela posição
        for obj in tmx_data.objects:
            if obj.x == pos[0] and obj.y == pos[1]:
                return obj.path
        return None

    def create_map(self, map_path):
        # Cria o mapa a partir de um arquivo TMX
        tmx_data = pytmx.load_pygame(map_path)
        self.visible_sprites.load_floor(tmx_data)
        self.process_layers(tmx_data)
        self.player = Player((self.get_pos(tmx_data, 'player')), [self.visible_sprites], self.obstacle_sprites)
        self.capecao = Capecao(self.player, (self.get_pos(tmx_data, 'capecao')))
        self.visible_sprites.add(self.capecao)
        self.visible_sprites.player = self.player

    def process_layers(self, tmx_data):
        # Processa as camadas do TMX
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.process_tiles(layer, tmx_data)

    def process_tiles(self, layer, tmx_data):
        # Processa os tiles de uma camada
        for x, y, gid in layer:
            if gid != 0:
                tile = tmx_data.get_tile_image_by_gid(gid)
                self.create_tile(layer.name, x, y, tile)

    def create_tile(self, layer_name, x, y, tile):
        # Cria um tile baseado na camada e posição
        position = (x * TILESIZE, y * TILESIZE)
        if layer_name == 'invisible':
            Tile(position, [self.visible_sprites], 'invisible')
        elif layer_name == 'grass':
            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'grass', tile)
        elif layer_name == 'objects':
            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'object', tile)
        elif layer_name == 'door':
            Tile(position, [self.visible_sprites, self.obstacle_sprites, self.doors], 'door', tile)
        elif layer_name == 'wall':
            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'wall', tile)

    def change_map(self, new_map_path):
        # Troca o mapa atual por um novo
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.doors.empty()
        self.visible_sprites.floor_tiles.clear()
        self.tmx_data = pytmx.load_pygame(new_map_path)
        self.create_map(new_map_path)

    def check_collision_with_door(self, tmx_data):
        # Verifica colisão com portas e troca de mapa
        for sprite in self.doors:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                if self.player.rect.colliderect(sprite.rect):
                    self.change_map(self.get_name(tmx_data, sprite.rect))

    def toggle_menu(self):
        # Não faz nada se o menu de desafio estiver ativo
        if self.show_challenge:
            return

        # Alterna o estado do menu de pausa
        self.game_paused = not self.game_paused
        self.player_can_move = not self.game_paused
        self.show_menu = self.game_paused  # Atualiza o estado de exibição do menu de pausa

    def start_challenge(self):
        # Inicia o desafio de ordenação apenas se não estiver ativo
        if not self.show_challenge and not self.show_menu:  # Verifica se o menu de pausa não está ativo
            self.game_paused = True
            self.show_challenge = True
            self.sorting_challenge.is_active = True
            self.player_can_move = False

    def toggle_challenge_menu(self):
        # Alterna o estado do menu de desafio
        self.sorting_challenge.toggle_menu()

    def complete_challenge(self):
        # Completa o desafio e reseta o estado do jogador
        self.game_paused = not self.game_paused
        self.show_challenge = False
        self.sorting_challenge.is_active = False
        self.reset_player_state()
        print("Desafio concluído! Avançando no jogo...")

    def reset_player_state(self):
        # Reseta o estado do jogador
        self.player_can_move = True

    def run(self):
        # Executa a lógica principal do nível
        self.visible_sprites.custom_draw(self.player)

        if self.game_paused:
            if self.show_challenge:
                self.sorting_challenge.display()
            else:
                self.pause_menu.display()
        else:
            self.visible_sprites.update()

        if self.challenge:
            self.challenge.display()

        self.check_collision_with_door(self.tmx_data)
        debug(self.game_paused)
        debug(self.player_can_move, 50)

class Room:
    def __init__(self):
        visited_rooms = []
        rooms = {
            'room0': ['room1_up', 'room1_down', 'room1_left', 'room1_right', 'room1_down_right'],
            'room1_up': ['room2_up_left', 'room2_up_right'],
            'room1_down': ['room2_left_down', 'room2_down'],
            'room1_left': ['room2_up_left', 'room2_left']
            'room1_right': ['room2_right']
            'room1_down_right': ['room2_down_right']

            'room2_up_left': ['room3_up_left', 'room3_up']
            'room2_up_right': ['room3_up_up_right']
            'room2_left_down': ['room3_down_left']
            'room2_down': ['room3_down_left', 'room3_down_right']
            'room2_right': ['room3_right_down', 'room3_right_left']
            'room2_down_right': ['room3_down_right']
            'room2_left': ['room3_left', 'room3_left_up', 'room3_left_down']

            'room3_up_left': []
            'room3_up': []
            'room3_up_up_right': []
            'room3_down_left': []
            'room3_down_right': []
            'room3_right_down': []
            'room3_right_left': []
            'room3_left': []
            'room3_left_up': []
            'room3_left_down': []

        }
        required_path = ['room1', 'room2', 'room4', 'room3']
    def visit_room(room):
        if room in rooms and (not visited_rooms or visited_rooms[-1] != room):
            visited_rooms.append(room)
            check_path()

    def bfs(start_room, target_room):
        visited = set()
        queue = deque([start_room])

        while queue:
            current_room = queue.popleft()
            if current_room == target_room:
                return True
            if current_room not in visited:
                visited.add(current_room)
                queue.extend(rooms[current_room])
        return False

    def check_path():
        if visited_rooms == required_path:
            print("Path completed successfully!")
        else:
            print(f"Current path: {visited_rooms}")

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # Inicialização do grupo de sprites com câmera
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_tiles = []

    def load_floor(self, tmx_data):
        # Carrega os tiles do chão a partir do TMX
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == 'floor':
                for x, y, gid in layer:
                    if gid != 0:
                        tile = tmx_data.get_tile_image_by_gid(gid)
                        position = (x * TILESIZE, y * TILESIZE)
                        self.floor_tiles.append((tile, position))

    def custom_draw(self, player):
        # Desenha os sprites com base na posição do jogador
        self.update_offset(player)
        self.draw_floor()
        self.draw_sprites()

    def update_offset(self, player):
        # Atualiza o offset da câmera baseado na posição do jogador
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def draw_floor(self):
        # Desenha os tiles do chão
        for tile, position in self.floor_tiles:
            offset_pos = pygame.math.Vector2(position) - self.offset
            self.display_surface.blit(tile, offset_pos)

    def draw_sprites(self):
        # Desenha os sprites na tela
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)