from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from menu import Menu
from dialogue import DialogBox
from challenge_sorting import SortingChallenge
import pytmx
from hanoi import Hanoi
from challenge_search import *
import random
import os
import math

class Level:
    def __init__(self, difficulty):
        # Inicialização de variáveis e grupos de sprites
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.puzzle = pygame.sprite.Group()
        self.npc = pygame.sprite.Group()
        self.create_light_mask()

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.font_small = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.dialogue = True

        # Inicialização de estados do jogo
        self.game_paused = False
        self.show_menu = False
        self.show_challenge = False
        self.show_dialogue = False
        self.player_can_move = True

        # Inicialização de dificuldade e mapa
        self.difficulty = difficulty
        self.map_name = 'room0'  # Nome do mapa atual

        # Inicialização de objetos de busca
        self.bfs_start = False
        self.bfs = BFS(self, self.difficulty, self.display_surface)  # Initialize BFS object
        self.dfs_start = False
        self.dfs = DFS(self, self.difficulty, self.display_surface)  # Initialize DFS object

        # Inicialização do jogador
        self.player = Player((100, 100), [self.visible_sprites], self.obstacle_sprites)


        # Criação do mapa inicial
        self.create_map('../map/start.tmx', player_pos=-1)
        self.tmx_data = pytmx.load_pygame('../map/start.tmx')

        # Inicialização de menus
        self.pause_menu = Menu(self)
        self.menu = Menu(self)
        self.dialog_box = DialogBox(self)

        # Inicialização de desafios
        self.challenge = None
        self.hanoi_challenge = Hanoi(self, self.display_surface, self.end_challenge, self.difficulty)
        self.sorting_challenge = SortingChallenge(self, self.difficulty)

        # Inicialização de cooldowns e interações
        self.door_cooldown = 1000  # Cooldown de 1 segundo
        self.last_door_interaction = pygame.time.get_ticks()

        # Inicialização de contadores
        self.completion = 0

    def create_light_mask(self):
        # Cria uma superfície preta com um buraco transparente no meio
        self.light_mask = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        self.light_mask.fill((0, 0, 0, 255))
        light_radius = 100
        light_center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
        pygame.draw.circle(self.light_mask, (0, 0, 0, 0), light_center, light_radius)

    def apply_light_mask(self):
        # Aplica a máscara de luz sobre o mapa
        player_pos = self.player.rect.center
        light_radius = 150
        light_center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
        mask_rect = self.light_mask.get_rect(center=light_center)
        self.display_surface.blit(self.light_mask, mask_rect.topleft)

    # Métodos de obtenção de posição e nome
    def get_pos(self, tmx_data, name):
        # Obtém a posição de um objeto no mapa pelo nome
        for obj in tmx_data.objects:
            if obj.name == name:
                print(obj.name)
                return obj.x, obj.y
        return 0, 0

    def get_name(self, tmx_data, pos):
        # Obtém o nome de um objeto no mapa pela posição
        for obj in tmx_data.objects:
            if obj.x == pos[0] and obj.y == pos[1]:
                return obj.path
        return None

    def replace_difficulty_in_path(self, path):
        if '{difficulty}' in path:
            new_path = path.replace('{difficulty}', self.difficulty)
            if os.path.exists(new_path):
                return new_path
        return path

    def get_player_new_location(self, tmx_data, pos):
        # Obtém o nome de um objeto no mapa pela posição
        for obj in tmx_data.objects:
            if obj.x == pos[0] and obj.y == pos[1]:
                print(obj.path)
                if hasattr(obj, 'player'):
                    return obj.player
        return False

    # Métodos de criação e processamento de mapa
    def create_map(self, map_path, player_pos):
        # Cria o mapa a partir de um arquivo TMX
        tmx_data = pytmx.load_pygame(map_path)
        self.visible_sprites.load_floor(tmx_data)
        self.process_layers(tmx_data)
        if player_pos == -1:
            player_pos = self.get_pos(tmx_data, 'player')
        else:
            player_pos = self.get_pos(tmx_data, player_pos)
        self.player = Player((player_pos), [self.visible_sprites], self.obstacle_sprites)
        self.visible_sprites.player = self.player
        self.map_name = map_path.split('/')[-1].split('.')[0]  # Atualiza o nome do mapa
        if self.map_name == "meet":
            self.dialogue = True

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
        elif layer_name == 'puzzle':
            Tile(position, [self.visible_sprites, self.obstacle_sprites, self.puzzle], 'door', tile)
        elif layer_name == 'npc':
            Tile(position, [self.visible_sprites, self.npc], 'npc', tile)

    def change_map(self, new_map_path, player_pos):
        new_map_path = self.replace_difficulty_in_path(new_map_path)
        # Clear all sprite groups
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.doors.empty()
        self.visible_sprites.floor_tiles.clear()

        # Load new map data
        self.tmx_data = pytmx.load_pygame(new_map_path)
        self.create_map(new_map_path, player_pos)

        self.visible_sprites.player = self.player

    # Métodos de verificação de colisão
    def check_collision_with_door(self, tmx_data):
        # Verifica colisão com portas e troca de mapa
        for sprite in self.doors:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                if self.player.rect.colliderect(sprite.rect):
                    door = self.get_name(tmx_data, sprite.rect)
                    if self.get_player_new_location(tmx_data,sprite.rect):
                        player_pos = self.get_player_new_location(tmx_data,sprite.rect)
                    else:
                        player_pos = -1
                    self.change_map(door, player_pos)

    def check_collision_with_puzzle(self, tmx_data):
        for sprite in self.puzzle:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                if self.player.rect.colliderect(sprite.rect):
                    if self.map_name == 'hanoi':
                        self.start_hanoi()
                    if self.map_name == 'sorting':
                        self.start_challenge()
                    if self.map_name == 'boss':
                        pass

    def check_collision_with_npc(self):
        pos = (self.player.rect.x, self.player.rect.y)
        for npc in self.npc:
            if self.player.rect.colliderect(npc.rect):
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_c] and not self.dialog_box.is_active) or self.dialogue:
                    self.dialogue = False
                    self.dialog_box.set_dialogue(self.map_name)
                    self.dialog_box.toggle_dialogue()
                    self.pause_game()


    # Métodos de controle de jogo
    def pause_game(self):
        self.game_paused = True
        self.player_can_move = False

    def resume_game(self):
        self.game_paused = False
        self.player_can_move = True

    def toggle_menu(self):
        # Não faz nada se o menu de desafio estiver ativo
        if self.show_challenge or self.show_dialogue:
            return

        # Alterna o estado do menu de pausa
        self.game_paused = not self.game_paused
        self.player_can_move = not self.game_paused
        self.show_menu = self.game_paused  # Atualiza o estado de exibição do menu de pausa

    # def end_challenge(self):
    #     self.game_paused = False
    #     self.show_challenge = False
    #     self.player_can_move = True

    def start_hanoi(self):
        # Inicia o desafio de ordenação apenas se não estiver ativo
        if not self.show_challenge and not self.show_menu:
            self.game_paused = True
            self.show_challenge = True
            self.sorting_challenge.is_active = False  # Desativa o desafio até que a dificuldade seja selecionada
            self.player_can_move = False
            self.hanoi_challenge.start()

    def start_challenge(self):
        # Inicia o desafio de ordenação apenas se não estiver ativo
        if not self.show_challenge and not self.show_menu:
            self.game_paused = True
            self.show_challenge = True
            self.sorting_challenge.is_active = False  # Desativa o desafio até que a dificuldade seja selecionada
            self.player_can_move = False

    def end_challenge(self):
        # Encerra o processo do desafio
        self.game_paused = not self.game_paused
        self.show_challenge = False
        self.reset_player_state()

    def mark_challenge_complete(self):
        # Adiciona +1 ao contador de desafios completos
        self.completion += 1

    def reset_player_state(self):
        # Reseta o estado do jogador
        self.player_can_move = True

    # Metodo principal de execução do nível
    def run(self):
        global DIFICULDADE
        # Executa a lógica principal do nível
        self.visible_sprites.custom_draw(self.player)

        if self.map_name == 'boss':
            self.apply_light_mask()

        if self.game_paused:
            if self.show_challenge:
                if self.map_name == 'hanoi':
                    self.hanoi_challenge.display()
                elif self.map_name == 'sorting':
                    self.sorting_challenge.display()
            elif self.show_dialogue:
                self.player_can_move = False
                self.dialog_box.display()
            else:
                self.pause_menu.display()
        else:
            self.visible_sprites.update()

        if self.challenge:
            self.challenge.display()

        #FOR DEBUG
        # self.completion = 5

        # BFS logic
        if self.map_name == 'room0' and self.completion != 5:
            self.bfs_start = True
            self.bfs.visit_room('room0')
            self.mapa_atual = self.map_name  # Initialize mapa_atual with the current map
        if self.bfs_start:
            if self.mapa_atual != self.map_name:
                self.bfs.visit_room(self.map_name)
                self.mapa_atual = self.map_name  # Initialize mapa_atual with the current map
                print(self.bfs.visited_rooms)
                print(self.bfs.required_path)
        if self.bfs.is_complete() and self.bfs_start:
            self.bfs_start = False
            self.bfs.visited_rooms.clear()
            self.bfs.current_tuple_index = 0
            self.bfs.current_tuple_visited.clear()
            self.change_map('../map/hub.tmx', player_pos=-1)
            self.bfs_start = False

        #DFS logic
        if self.map_name == 'node0':
            self.dfs_start = True
            #self.dfs.visit_room('room0')
            self.mapa_atual = self.map_name  # Initialize mapa_atual with the current map
        if self.dfs_start:
            if self.mapa_atual != self.map_name:
                if self.dfs.visit_room(f"{self.map_name}") == 'perdeu':
                    self.dfs.visited_rooms.clear()
                    self.change_map('../map/hub.tmx', player_pos=-1)
                    self.dfs_start = False
                self.mapa_atual = self.map_name  # Initialize mapa_atual with the current map
                print(f"{self.dfs.rooms}")
                print(f"Current path: {self.dfs.visited_rooms}")
                if self.map_name == 'hub.tmx':
                    self.dfs.visited_rooms.clear()
                #print(self.bfs.visited_rooms)
                #print(self.bfs.required_path)
        if self.dfs.is_complete() and self.dfs_start:
            self.dfs_start = False
            self.dfs.visited_rooms.clear()
            self.dfs.current_tuple_index = 0
            self.change_map('../map/hub.tmx', player_pos=-1)
            self.dfs_start = False

        self.check_collision_with_puzzle(self.tmx_data)
        self.check_collision_with_door(self.tmx_data)
        self.check_collision_with_npc()


        score_surf = self.font.render(f"Score: {self.completion}", True, WHITE)
        score_rect = score_surf.get_rect(topleft=(10, 10))
        self.display_surface.blit(score_surf, score_rect)
        #debug(self.completion, 50)
        #debug(self.difficulty, 100)
        # debug(f"game_paused: {self.game_paused}")
        # debug(f"player_can_move: {self.player_can_move}", 50)
        # debug(f"Current map: {self.map_name}", 150)  # Adiciona a linha de debug para o nome do mapa

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
            """""
            if hasattr(sprite, 'hitbox'):
                hitbox_rect = sprite.hitbox.copy()
                hitbox_rect.topleft = hitbox_rect.topleft - self.offset
                pygame.draw.rect(self.display_surface, (255, 0, 0), hitbox_rect, 2)  # Desenha o retângulo em vermelho
            """""
