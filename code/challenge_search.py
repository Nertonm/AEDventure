from collections import deque
from itertools import permutations


class BFS:
    def __init__(self,difficulty='easy', display_surface=None):
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
            return True
        else:
            print(f"Current path: {self.visited_rooms}")

class DFS:
    def __init__(self, difficulty='medium', display_surface=None):
        self.difficulty = difficulty
        self.display_surface = display_surface
        self.win = False
        self.lost = False
        self.visited_rooms = ['node0']
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
        if difficulty == 'medium':
            self.rooms = {
                'room0': ['room1_up', 'room1_down', 'room1_left', 'room1_right', 'room1_down_right'],
                'room1_up': ['room2_up_left', 'room2_up_right'],
                'room1_down': ['room2_left_down', 'room2_down'],
                'room1_left': ['room2_up_left', 'room2_left'],
                'room1_right': ['room2_right', 'room2_up_right'],
                'room1_down_right': ['room2_down_right', 'room2_right'],
                'room2_up_left': [],
                'room2_up_right': [],
                'room2_left_down': [],
                'room2_down': [],
                'room2_right': [],
                'room2_down_right': [],
                'room2_left': [],
            }
        elif difficulty == 'easy':
            self.rooms = [('node0','nodeb', 'nodec' 'nodea' ), ('node0','nodeb', 'noded' 'nodea'),
                          ('node0','nodeb', 'nodea')]
            self.qnt_nodes = 5

    def is_complete(self):
        return self.win

    def is_dfs_subpath(self):
        required_sequences = self.rooms
        for sequence in required_sequences:
            if self.visited_rooms == list(sequence):
                return False
        return True

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
                        print("Path completed successfully!")
                        return True
                    else:
                        print("Graph not fully traversed yet.")
                        return False
                else:
                    print(f"{room} is not part of a valid DFS path!")
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



