from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
import pytmx


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.create_map('../map/map.tmx')
        self.tmx_data = pytmx.load_pygame('../map/map.tmx')

    def get_pos(self, tmx_data, name):
        for obj in tmx_data.objects:
            if obj.name == name:
                return obj.x, obj.y
        return 0, 0

    def get_name(self,tmx_data, pos):
        print(pos[0], pos[1])
        for obj in tmx_data.objects:
            if obj.x == pos[0] and obj.y == pos[1]:
                print("DADADAfa")
                print(obj.path)
                return obj.path
        return None

    def create_map(self, map_path):
        tmx_data = pytmx.load_pygame(map_path)
        self.visible_sprites.load_floor(tmx_data)
        self.process_layers(tmx_data)
        self.player = Player((self.get_pos(tmx_data, 'player')), [self.visible_sprites], self.obstacle_sprites)
        self.visible_sprites.player = self.player

    def process_layers(self, tmx_data):
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.process_tiles(layer, tmx_data)

    def process_tiles(self, layer, tmx_data):
        for x, y, gid in layer:
            if gid != 0:
                tile = tmx_data.get_tile_image_by_gid(gid)
                self.create_tile(layer.name, x, y, tile)

    def create_tile(self, layer_name, x, y, tile):
        position = (x * TILESIZE, y * TILESIZE)
        if layer_name == 'boundary':
            Tile(position, [self.obstacle_sprites], 'invisible')
        elif layer_name == 'grass':
            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'grass', tile)
        elif layer_name == 'object':
            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'object', tile)
        elif layer_name == 'door':
            Tile(position, [self.visible_sprites, self.obstacle_sprites, self.doors], 'door', tile)
        elif layer_name == 'wall':
            Tile(position, [self.visible_sprites], 'wall', tile)

    def change_map(self, new_map_path):
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.doors.empty()
        self.visible_sprites.floor_tiles.clear()
        self.tmx_data = pytmx.load_pygame(new_map_path)
        self.create_map(new_map_path)

    def check_collision_with_door(self, tmx_data):
        for sprite in self.doors:
            keys = pygame.key.get_pressed()
            debug(keys, 100, 100)
            if keys[pygame.K_e]:
                if self.player.rect.colliderect(sprite.rect):
                    print("DADADAfa")
                    self.change_map(self.get_name(tmx_data, sprite.rect))

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.check_collision_with_door(self.tmx_data)
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_tiles = []

    def load_floor(self, tmx_data):
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == 'floor':
                for x, y, gid in layer:
                    if gid != 0:
                        tile = tmx_data.get_tile_image_by_gid(gid)
                        position = (x * TILESIZE, y * TILESIZE)
                        self.floor_tiles.append((tile, position))

    def custom_draw(self, player):
        self.update_offset(player)
        self.draw_floor()
        self.draw_sprites()

    def update_offset(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def draw_floor(self):
        for tile, position in self.floor_tiles:
            offset_pos = pygame.math.Vector2(position) - self.offset
            self.display_surface.blit(tile, offset_pos)

    def draw_sprites(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite != self.player:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
            offset_pos = self.player.rect.topleft - self.offset
            self.display_surface.blit(self.player.image, offset_pos)