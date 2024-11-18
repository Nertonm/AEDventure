import pygame
import sys
from settings import *
from level import Level
from menu import *
from dialogue import DialogBox  # Import the DialogBox class

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('AEDventure')
        self.clock = pygame.time.Clock()
        self.level = None
        self.dialog_box = None
        self.opening_screen = OpeningScreen(self.screen)
        self.show_opening = True

    def run(self):
        global DIFFICULTY
        while self.show_opening:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_result = self.opening_screen.check_click(event)
                key_result = self.opening_screen.check_key(event)
                if click_result == "start_game" or key_result == "start_game":
                    DIFFICULTY = self.opening_screen.selected_difficulty
                    print(DIFFICULTY)
                    self.level = Level(DIFFICULTY)  # Pass the updated difficulty
                    self.dialog_box = DialogBox(self.screen, self.level)  # Initialize DialogBox
                    self.show_opening = False
                elif click_result == "exit" or key_result == "exit":
                    pygame.quit()
                    sys.exit()

            self.opening_screen.display()
            self.clock.tick(FPS)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level.show_challenge and not self.level.sorting_challenge.is_active:
                        self.level.sorting_challenge.check_difficulty_selection(event)
                    else:
                        self.level.sorting_challenge.check_button_click(event)
                        self.level.pause_menu.check_mouse_click(event)

                self.dialog_box.check_trigger(event)  # Check for dialog box trigger

            self.screen.fill('black')
            self.level.run()
            if self.dialog_box.is_active:
                self.dialog_box._draw()  # Draw the dialog box if active
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()