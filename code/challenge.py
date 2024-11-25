import pygame
from settings import *
from debug import debug


class Challenge:

    def __init__(self, level, difficulty):
        # Usage at Level.__init__: self.challenge = Challenge(self, self.difficulty)

        # Game settings
        self.level = level
        self.difficulty = difficulty
        self.is_active = True
        self.success = False  # == self.challenge_completed
        self.failure = False

        # Specific Settings
        if difficult == 'easy':
            self.tamanho = [4, 4]
        elif difficult == 'medium':
            self.tamanho = [6, 6]
        else:
            self.tamanho = [8, 8]
        # tamanho do espaço entre linhas
        self.size = 33
        self.img_new = Image.new('RGBA', (self.tamanho[0] * (self.size + 1) + 1, self.tamanho[1] * (self.size + 1) + 1), (0, 0, 0, 0))
        self.size += 1
        self.id_quadrado = 0
        self.cor = [randint(15, 255), randint(15, 255), randint(15, 255)]
        self.draw = ImageDraw.Draw(self.img_new)
        self.fundo = pygame.image.load("rect.png")
        self.fundo_rect = self.fundo.get_rect(topleft=(0, 0))
        self.img = self.img_new.convert('RGB')
        self.rgb = self.img.load()
        self.img_width, self.img_height = self.img.size
        self.posicoes = {id_quadrado: [[self.tamanho[0] * self.size - self.size / 2, self.size / 2], [randint(15, 255), randint(15, 255), randint(15, 255)]}
        self.buttons = {
            "up": pygame.Rect(50, 400 - 80, 100, 50),
            "down": pygame.Rect(160, 400 - 80, 100, 50),
            "left": pygame.Rect(270, 400 - 80, 100, 50),
            "right": pygame.Rect(380, 400 - 80, 100, 50),
            "enter": pygame.Rect(490, 400 - 80, 100, 50)
        }
        self.button_order = ["up", "down", "left", "right", "enter"]
        self.selected_button = 0
        movimentos_stack = []

        # Graphics settings
        self.display_surface = pygame.display.get_surface()

        # UI
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.font_small = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.selected_button = None  # Adiciona o botão selecionado

        # Close Button
        button_width = 100
        button_height = 50
        self.close_button = pygame.Rect(
            (self.display_surface.get_width() - button_width) // 2,
            self.display_surface.get_height() - button_height - 10,
            button_width, button_height)

    @property
    def challenge_completed(self):
        return self.success

    @challenge_completed.setter
    def challenge_completed(self, value: bool):
        if type(value) == bool:
            self.success = value
        else:
            raise ValueError("challenge_completed must be boolean")

    # def generate_something(self): ...
    def gerar_labirinto(w=10, h=10):
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]: continue
                if xx == x: hor[max(y, yy)][x] = "+  "
                if yy == y: ver[y][max(x, xx)] = "   "
                walk(xx, yy)

        walk(randrange(w), randrange(h))
        linhas_colunas = [[], []]
        for (a, b) in zip(hor, ver):
            # print(''.join(a + ['\n'] + b), flush=True)
            for l in a:
                if l == "+--":
                    linhas_colunas[0].append(1)
                elif l == "+":
                    pass
                else:
                    linhas_colunas[0].append(0)
            if len(b) != 0:
                for c in b:
                    if "|" in c:
                        linhas_colunas[1].append(1)
                    else:
                        linhas_colunas[1].append(0)

    def desenhar_labirinto_pillow(self, img, tamanho, posicoes, size=11):
        (x, y) = tamanho
        size = size + 1
        contX = contY = 0
        cor = (255, 255, 255)
        for yy in range(0, y * size + 1, size):
            for xx in range(0, x * size + 1, size):
                try:
                    if self.array[contY][contX] == 1:
                        img.rectangle((xx, yy, xx + size, yy + size), fill=(0, 0, 0), outline=(0, 0, 0))
                    else:
                        img.rectangle((xx, yy, xx + size, yy + size), fill=(255, 255, 255), outline=(255, 255, 255))
                    contX += 1
                except IndexError:
                    pass
            contY += 1
            contX = 0
        # desenha_fim_pillow(img, tamanho, size)
        return img

    def desenha_fim_pillow(self, tela, tamanho, size=11):
        (x, y) = tamanho
        tela.rectangle((1, y * size - size + 1, size - 1, y * size - 1), fill=(255, 0, 0), outline=(255, 0, 0))

    def draw_buttons(self):
        for i, (text, rect) in enumerate(self.buttons.items()):
            color = (0, 0, 0) if i != self.selected_button else (255, 0, 0)
            pygame.draw.rect(self.display_surface, color, rect)
            label = self.font.render(text, True, (255, 255, 255))
            self.display_surface.blit(label, (rect.x + 10, rect.y + 10))

    def move_cima(self, rgb, size, posicoes, id_jogador):
        posicoes, jogou = cima(rgb, size, posicoes, id_jogador)
        if jogou:
            print('up')
        return posicoes, jogou

    def move_baixo(self, rgb, size, posicoes, id_jogador):
        posicoes, jogou = baixo(rgb, size, posicoes, id_jogador)
        if jogou:
            print('down')
        return posicoes, jogou

    def move_esquerda(self, rgb, size, posicoes, id_jogador):
        posicoes, jogou = esquerda(rgb, size, posicoes, id_jogador)
        if jogou:
            print('left')
        return posicoes, jogou

    def move_direita(self, rgb, size, posicoes, id_jogador):
        posicoes, jogou = direita(rgb, size, posicoes, id_jogador)
        if jogou:
            print('right')
        return posicoes, jogou

    def process_movements(self):
        while self.stack:
            direction = self.stack.pop()
            if direction == "up":
                self.cima()
                print("cima")
            elif direction == "down":
                self.baixo()
                print('baixo')
            elif direction == "left":
                self.esquerda()
                print('esquerda')
            elif direction == "right":
                self.direita()
                print('direita')
            self.posicionar_jogadores(self.tela, self.posicoes, self.size)
            pg.display.update()
            sleep(0.5)
    # def start(self): ...

    def toggle_menu(self):
        # Alterna o estado do menu de desafio
        self.is_active = not self.is_active
        if not self.is_active:
            self.level.reset_player_state()

    def input(self):
        # Gerencia a entrada do usuário

        keys = pygame.key.get_pressed()
        # current_time = pygame.time.get_ticks()
        # enter_cooldown = 200

        # Reinicia o do puzzle se o jogador falhar e pressionar Enter
        if self.failure:
            # if keys[pygame.K_RETURN] and current_time - self.last_enter_time >= enter_cooldown:
            if keys[pygame.K_RETURN]:
                self.failure = False
                self.is_active = True
                # Put here your Resetting Code
            return

        # Inativo ou completo
        if not self.is_active or self.success:
            return

        # Put here your specific input code
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self_selected_button = (self.selected_button - 1) % len(self.button_order)
                    if event.key == pygame.K_RIGHT:
                        self.selected_button = (self.selected_button + 1) % len(self.button_order)
                    if event.key == pygame.K_RETURN:
                        if self.button_order[self.selected_button] == "up":
                            self.movements_stack.append("up")
                        elif self.button_order[self.selected_button] == "down":
                            self.movements_stack.append("down")
                        elif self.button_order[self.selected_button] == "left":
                            self.movements_stack.append("left")
                        elif self.button_order[self.selected_button] == "right":
                            self.movements_stack.append("right")
                        elif self.button_order[self.selected_button] == "enter":
                            self.process_movements()
                self.check_button_click(event)


    def reset_with_failure(self):
        ...

    def is_solved(self):
        ...

        if ...:
            self.success = True
            self.level.mark_challenge_complete(self.__class__)
            self.challenge_completed = True

    def check_button_click(self, event):
        if not self.is_active:
            return
        # Verifica se o botão foi clicado
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Botão de fechar
            if self.close_button.collidepoint(event.pos):
                if self.failure:
                    # Reinicia o estado do jogo se o jogador falhar e clicar em "Try Again"
                    self.failure = False
                    self.is_active = True
                    ...
                else:
                    self.is_active = False
                    self.level.reset_player_state()
                    # Garante que o menu de desafio não esteja ativo
                    self.level.show_challenge = False
                    # self.level.<nome do desafio>_challenge.is_active = False
                    self.success = False
                    self.failure = False
                    self.level.end_challenge()

            # Outros botões aqui!
            ...

    def check_button_hover(self):
        # Verifica se o mouse está sobre o botão
        mouse_pos = pygame.mouse.get_pos()
        self.button_hovered = self.close_button.collidepoint(mouse_pos)

    def check_won(self, posicao, tamanho, size):
        for ID, p in posicao.items():
            if p[0] == [size / 2, tamanho[1] * size - size / 2]:
                return True

        return False

    def display(self):
        if not self.is_active:
            self.display_difficulty_selection()
            return

        self.input()
        self.check_button_hover()

        surface = pygame.Surface(
            self.display_surface.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.display_surface.blit(surface, (0, 0))

        if not self.success and not self.failure:
            ...#codigo do jogo
            draw_buttons()
            for event in event.get():
                if event.type == QUIT:
                    self.is_active = False
                    self.level.reset_player_state()
                    self.level.show_challenge = False
                    self.level.end_challenge()
                self.check_button_click(event)
            vencedor = self.check_won(posicao, tamanho, size)
            pygame.draw.rect(tela, cor, ((x - size / 2 + 1, y - size / 2 + 1), (size - 1, size - 1)))
            pygame.display.update()
            if vencedor:
                exit()
        # Close Button Render

        if self.failure:
            close_button_text = "Try Again"
            button_color = (
                0, 255, 0) if self.button_hovered or self.button_selected else (255, 0, 0)
        else:
            close_button_text = "Close"
            button_color = (
                0, 255, 0) if self.button_hovered or self.button_selected else (255, 0, 0)

        button_text_surf = self.font.render(
            close_button_text, True, (255, 255, 255))
        button_text_rect = button_text_surf.get_rect(
            center=self.close_button.center)
        self.close_button = button_text_rect
        pygame.draw.rect(self.display_surface,
                         button_color, self.close_button)
        self.display_surface.blit(button_text_surf, button_text_rect)

        # Success/Failure message

        if self.success:
            message_surf = self.font.render(
                "Congratulations!", True, (0, 255, 0))
            message_rect = message_surf.get_rect(
                center=self.display_surface.get_rect().center)
            self.display_surface.blit(message_surf, message_rect)
        elif self.failure:
            message_surf = self.font.render(
                "You fail!", True, (255, 0, 0))
            message_rect = message_surf.get_rect(
                center=self.display_surface.get_rect().center)
            self.display_surface.blit(message_surf, message_rect)

        # Exibe a mensagem se o desafio já foi completado
        if self.challenge_completed:
            completed_message = "You have completed this challenge."
            completed_message_surf = self.font_small.render(
                completed_message, True, (255, 255, 0))
            completed_message_rect = completed_message_surf.get_rect(
                center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 100))
            self.display_surface.blit(
                completed_message_surf, completed_message_rect)

        # debug(self.array, 500)
        pygame.display.update()
