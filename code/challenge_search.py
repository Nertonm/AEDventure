from collections import deque
from itertools import permutations
import pygame

class BFS:
    def __init__(self, level, difficulty='easy', display_surface=None):
        self.level = level
        self.difficulty = difficulty
        self.display_surface = display_surface
        self.win = False
        self.visited_rooms = []
        self.rooms = {
            'room0': ['room1_up', 'room1_down', 'room1_left', 'room1_right', 'room1_down_right'],
            'room1_up': ['room2_up_left', 'room2_up_right'],
            'room1_down': ['room2_left_down', 'room2_down'],
            'room1_left': ['room2_up_left', 'room2_left'],
            'room1_right': ['room2_right', 'room2_up_right'],
            'room1_down_right': ['room2_down_right', 'room2_right'],
            'room2_up_left': ['room3_up_left', 'room3_up'],
            'room2_up_right': ['room3_up_right', 'room3_up'],
            'room2_left_down': ['room3_down_left'],
            'room2_down': ['room3_down_left', 'room3_down_right'],
            'room2_right': ['room3_right_down', 'room3_right_up'],
            'room2_down_right': ['room3_down_right'],
            'room2_left': ['room3_left', 'room3_left_up', 'room3_left_down'],
            'room3_up_left': [],
            'room3_up': [],
            'room3_up_right': [],
            'room3_down_left': [],
            'room3_down_right': [],
            'room3_right_down': [],
            'room3_right_up': [],
            'room3_left': [],
            'room3_left_up': [],
            'room3_left_down': [],
        }
        if difficulty == 'hard':
            self.required_path = [('room0'),
                                  ('room1_up', 'room1_down', 'room1_left', 'room1_right',
                                   'room1_down_right'), ('room2_up_left',
                                'room2_up_right', 'room2_left_down', 'room2_down',
                                'room2_right', 'room2_down_right', 'room2_left'),
                                ('room3_up_left','room3_up','room3_up_right',
                               'room3_down_left','room3_down_right','room3_right_down',
                               'room3_right_left','room3_left','room3_left_up','room3_left_down')]
        elif difficulty == 'medium':
            self.required_path = [('room0'),
                                  ('room1_up', 'room1_down', 'room1_left', 'room1_right',
                                   'room1_down_right'), ('room2_up_left',
                                'room2_up_right', 'room2_left_down', 'room2_down',
                                'room2_right', 'room2_down_right', 'room2_left')]
        elif difficulty == 'easy':
            self.required_path = [('room0'),
                                ('room1_up','room1_down', 'room1_left', 'room1_right',
                                'room1_down_right')]
        self.current_tuple_index = 0
        self.current_tuple_visited = set()

    def is_complete(self):
        return self.win

    def check_completed(self):
        if self.win == True:
            self.level.mark_challenge_complete()

    def visit_room(self, room):
        if self.win == False:
            current_tuple = self.required_path[self.current_tuple_index]
            if isinstance(current_tuple, tuple):
                if (room not in current_tuple) and (room not in self.visited_rooms):
                    print("Caminho errado")
                    return False
            else:
                if room != current_tuple:
                    print("Caminho errado")
                    return False

            if room in self.rooms:
                if room not in self.visited_rooms:
                    self.visited_rooms.append(room)
                    self.current_tuple_visited.add(room)
                    self.check_path()
                return True
            print("Caminho errado")
            return False
    def bfs(self, start_room, target_room):
        visited = set()
        queue = deque([start_room])

        while queue:
            current_room = queue.popleft()
            if current_room == target_room:
                return True
            if current_room not in visited:
                visited.add(current_room)
                queue.extend(self.rooms[current_room])
        return False

    def check_path(self):
        current_tuple = self.required_path[self.current_tuple_index]
        if isinstance(current_tuple, tuple):
            if all(room in self.current_tuple_visited for room in current_tuple):
                self.current_tuple_index += 1
                self.current_tuple_visited.clear()
        else:
            if current_tuple in self.current_tuple_visited:
                self.current_tuple_index += 1
                self.current_tuple_visited.clear()

        if self.current_tuple_index == len(self.required_path):
            print("Path completed successfully!")
            self.win = True
            self.check_completed()
            return True
        else:
            print(f"Current path: {self.visited_rooms}")

class DFS:
    def __init__(self, level, difficulty='medium', display_surface=None):
        self.level = level
        self.difficulty = difficulty
        self.display_surface = display_surface
        self.win = False
        self.lost = False
        self.failure_message = "You failed!"
        self.font = pygame.font.Font(None, 36)
        self.visited_rooms = ['node0']
        self.rooms = ['node0', 'nodea', 'nodeb', 'nodec', 'noded']
        self.qnt_nodes = 5
        if self.difficulty == 'medium':
            self.rooms = ['node0', 'nodea', 'nodec', 'noded', 'nodeb', 'nodee', 'nodeg', 'nodef']
            self.qnt_nodes = 8
        elif self.difficulty == 'hard':
            self.rooms = ['node0', 'nodea', 'nodec', 'noded', 'nodeb', 'nodee', 'nodeg', 'nodef']
            self.qnt_nodes = 8

    def is_complete(self):
        return self.win

    def check_completed(self):
        if self.win == True:
            self.level.mark_challenge_complete()

    def is_dfs_subpath(self):
        required_sequence = self.rooms[:len(self.visited_rooms)]
        return self.visited_rooms == required_sequence

    def is_graph_fully_traversed(self):
        if len(self.visited_rooms) == self.qnt_nodes:
            return True
        return False

    def visit_room(self, room):
        if not self.win:
            if self.add_room(room):
                if self.is_dfs_subpath():
                    if self.is_graph_fully_traversed():
                        self.win = True
                        self.check_completed()
                        print("Path completed successfully!")
                        return True
                    else:
                        print("Graph not fully traversed yet.")
                        return False
                else:
                    print(f"{room} is not part of a valid DFS path!")
                    message_surf = self.font.render(self.failure_message, True, (255, 0, 0))
                    message_rect = message_surf.get_rect(center=self.display_surface.get_rect().center)
                    self.display_surface.blit(message_surf, message_rect)
                    self.lost = True
                    print("Wrong path!")
                    return False
            else:
                print(f"{room} has already been visited.")
                return False

    def add_room(self, new_room):
        if new_room not in self.visited_rooms:
            self.visited_rooms.append(new_room)
            print(f"{new_room} adicionado!")
            return True
        else:
            return False

if __name__ == '__main__':
    dfs_instance = DFS(difficulty='medium')
    dfs_instance.visit_room("room0")
    dfs_instance.visit_room("room1_up")
    dfs_instance.visit_room("room1_down")
    dfs_instance.visit_room("room1_down")
    dfs_instance.visit_room("room1_left")
    dfs_instance.visit_room("room1_down_right")
    dfs_instance.visit_room("room1_right")



