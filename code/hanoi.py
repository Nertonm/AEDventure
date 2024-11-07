import pygame, sys, time

class Hanoi:
    def __init__(self, display_surface, end_challenge_callback):
        # Variáveis utilizadas pro funcionamento
        self.n_disks = 3
        self.disks = []
        self.steps = 0
        self.pointing_at = 0
        self.floating = False
        self.floater = 0
        self.display_surface = display_surface
        self.towers_midx = [display_surface.get_width() // 2 - 200, display_surface.get_width() // 2, display_surface.get_width() // 2 + 200]
        self.clock = pygame.time.Clock()
        self.end_challenge_callback = end_challenge_callback

        # Posições das torres
        self.towers_midx = [120, 320, 520]

        # Cores
        self.white, self.grey, self.blue, self.green = (255, 255, 255), (170, 170, 170), (78, 162, 196), (77, 206, 145)


    def make_disks(self):
        self.disks = []
        height, width, ypos = 20, self.n_disks * 23, 397 - 20
        for i in range(self.n_disks):
            self.disks.append({'rect': pygame.Rect(0, 0, width, height), 'val': self.n_disks - i, 'tower': 0})
            self.disks[-1]['rect'].midtop = (self.towers_midx[0], ypos)
            width -= 23
            ypos -= height + 3

    def draw_towers(self):
        for xpos in self.towers_midx:
            pygame.draw.rect(self.display_surface, self.green, pygame.Rect(xpos - 80, 400, 160, 20))
            pygame.draw.rect(self.display_surface, self.grey, pygame.Rect(xpos - 5, 200, 10, 200))

    def draw_disks(self):
        for disk in self.disks:
            pygame.draw.rect(self.display_surface, self.blue, disk['rect'])

    def draw_ptr(self):
        pygame.draw.polygon(self.display_surface, (255, 0, 0), [(self.towers_midx[self.pointing_at]-7 ,440), (self.towers_midx[self.pointing_at]+7, 440), (self.towers_midx[self.pointing_at], 433)])

    def check_won(self):
        if all(disk['tower'] == 2 for disk in self.disks):
            time.sleep(0.2)
            self.end_challenge_callback()
            return True

    #def reset():
    #    global steps, pointing_at, floating, floater
    #    steps, pointing_at, floating, floater = 0, 0, False, 0
    #    make_disks()

    def start(self):
        self.make_disks()

    def display(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.start()
                    if event.key == pygame.K_RIGHT:
                        self.pointing_at = (self.pointing_at + 1) % 3
                        if self.floating:
                            self.disks[self.floater]['rect'].midtop = (self.towers_midx[self.pointing_at], 100)
                            self.disks[self.floater]['tower'] = self.pointing_at
                    if event.key == pygame.K_LEFT:
                        self.pointing_at = (self.pointing_at - 1) % 3
                        if self.floating:
                            self.disks[self.floater]['rect'].midtop = (self.towers_midx[self.pointing_at], 100)
                            self.disks[self.floater]['tower'] = self.pointing_at
                    if event.key == pygame.K_UP and not self.floating:
                        for disk in reversed(self.disks):
                            if disk['tower'] == self.pointing_at:
                                self.floating, self.floater = True, self.disks.index(disk)
                                disk['rect'].midtop = (self.towers_midx[self.pointing_at], 100)
                                break
                    if event.key == pygame.K_DOWN and self.floating:
                        for disk in reversed(self.disks):
                            if disk['tower'] == self.pointing_at and self.disks.index(disk) != self.floater:
                                if disk['val'] > self.disks[self.floater]['val']:
                                    self.floating = False
                                    self.disks[self.floater]['rect'].midtop = (self.towers_midx[self.pointing_at], disk['rect'].top - 23)
                                    self.steps += 1
                                break
                        else:
                            self.floating = False
                            self.disks[self.floater]['rect'].midtop = (self.towers_midx[self.pointing_at], 400 - 23)
                            self.steps += 1

                # Cria uma superfície semi-transparente
                overlay = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
                overlay.fill((0, 0, 128))
                self.display_surface.blit(overlay, (0, 0))

                self.display_surface.fill(self.white)
                self.draw_towers()
                self.draw_disks()
                self.draw_ptr()

                pygame.display.flip()

                if not self.floating:
                    if self.check_won():
                        running = False
                        break

                self.clock.tick(60)