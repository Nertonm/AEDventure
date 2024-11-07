import pygame
from support import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, position, attack_range=100, attack_damage=10):
        super().__init__()

        # Inicia a imagem e o rect do inimigo
        self.image = pygame.image.load('../graphics/monsters/raccon/0.png').convert_alpha()  # Imagem padrão
        self.rect = self.image.get_rect(topleft=position)

        # Inicialização dos gráficos e animações
        self.import_enemy_assets()
        self.status = 'right_idle'  # Status inicial de animação
        self.frame_index = 0
        self.animation_speed = 0.15  # Velocidade de animação

        # Movimentação e controle de direção
        self.direction = pygame.math.Vector2()
        self.player = player  # Referência ao jogador
        self.speed = 3  # Velocidade de movimento do inimigo
        self.position = pygame.math.Vector2(position)  # Posição do inimigo

        # Parâmetros de ataque
        self.attack_range = attack_range  # Raio de ataque
        self.attack_damage = attack_damage  # Dano do ataque

        # Tempo de cooldown de ataque
        self.attack_cooldown = 1000  # 1 segundo de cooldown
        self.last_attack_time = 0

    def import_enemy_assets(self):
        # Carrega as animações do inimigo
        enemy_path = '../graphics/monsters/'
        self.animations = {'left': [], 'right': [], 'right_idle': [], 'left_idle': []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        # Animação do inimigo baseada no status atual
        animation = self.animations[self.status]

        # Avança o índice da animação
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Atualiza a imagem
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_towards_player(self):
        # Calcula a direção para o jogador
        player_position = pygame.math.Vector2(self.player.rect.center)
        distance_to_player = player_position - self.position

        if distance_to_player.length() <= self.attack_range:
            # Inicia ataque se estiver dentro do alcance
            self.attack_player()
        else:
            # Move em direção ao jogador
            direction = distance_to_player.normalize()  # Direção normalizada
            self.position += direction * self.speed  # Atualiza a posição

            # Atualiza o status com base no movimento
            if abs(direction.x) > abs(direction.y):
                self.status = 'right' if direction.x > 0 else 'left'
            else:
                self.status = 'right' if direction.y > 0 else 'left'

    def attack_player(self):
        # Verifica se o inimigo pode atacar
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            # Realiza o ataque
            print(f"Enemy attacks the player! Damage: {self.attack_damage}")
            self.last_attack_time = current_time
            # Aqui você pode adicionar lógica de dano ao jogador
            self.status = 'right_idle'  # Exemplo: mudar para animação de ataque

    def update(self):
        # Atualiza animação e movimento
        self.animate()
        self.move_towards_player()
