class BFS:
    def __init__(self, display_surface, difficulty):
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