import random, copy

class Minesweeper():
    # This is my minesweeper game!
    def __init__(self, board_size: int, bomb_count: int):
        self.board_size = board_size
        self.bomb_count = bomb_count
        self.bomb_board = []
        self.info_board = []
        self.visible_board = []
        self.player_board = []
        self.OPEN = "O"
        self.CLOSED = "X"
        self.SURROUNDING_COORDINATES = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,-1), (-1,1)]
        self.selected_tiles = 0
    
    def create_board(self):
        self.bomb_board = [[0 for i in range(self.board_size)] for i in range(self.board_size)]
        self.visible_board = [[self.CLOSED for i in range(self.board_size)] for i in range(self.board_size)]
        self.player_board = [[self.CLOSED for i in range(self.board_size)] for i in range(self.board_size)]

        self.generate_bomb_positions()
        self.info_board = copy.deepcopy(self.bomb_board)
        #print("self.bomb_board:",self.bomb_board)
        self.calculate_info_board_tiles()
        #print(self.info_board)
    
    def generate_bomb_positions(self) -> list:
        bomb_positions = []
        while len(bomb_positions) < self.bomb_count:
            curr_bomb_pos = (random.randint(0, self.board_size-1), random.randint(0, self.board_size-1))
            if curr_bomb_pos not in bomb_positions:
                bomb_positions.append(curr_bomb_pos)
        
        #print("bomb_positions:",bomb_positions)

        for bomb_pos in bomb_positions:
            self.bomb_board[bomb_pos[0]][bomb_pos[1]] = -1

    def calculate_info_board_tiles(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                if self.info_board[row][column] == -1:
                    continue
                
                sum_of_tile_surroundings = self.calculate_tile_surroundings((row, column))
                self.info_board[row][column] = sum_of_tile_surroundings
    
    def calculate_tile_surroundings(self, pos: tuple) -> int:
        sum = 0
        for direction in self.SURROUNDING_COORDINATES:
            try:
                x, y = pos[0]-direction[0], pos[1]-direction[1]
                
                if x < 0 or y < 0:
                    continue

                sum = sum - self.bomb_board[x][y]
            except IndexError:
                #print("Position: (",pos[0]-direction[0],",",pos[1]-direction[1],") is invalid")
                pass
        return sum

    def calculate_player_board_tiles(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                if self.visible_board[row][column] == self.OPEN:
                    self.player_board[row][column] = self.info_board[row][column]

    def select_square(self, pos: tuple) -> bool:
        self.selected_tiles += 1

        if (pos[0] > self.board_size-1 or pos[0] < 0 or pos[1] > self.board_size-1 or pos[1] < 0):
            return False
        
        if (self.bomb_board[pos[0]][pos[1]]):
            if (self.selected_tiles == 1):
                while self.select_square(pos):
                    #print("board regenerated")
                    self.create_board()
                return False
            return True
        
        self.visible_board[pos[0]][pos[1]] = self.OPEN

        new_tiles_to_make_visible = []
        list_of_zero_tiles = self.get_adjacent_zero_tiles(pos)
        list_of_non_zero_tiles = self.get_adjacent_non_zero_tiles(list_of_zero_tiles)
        new_tiles_to_make_visible.extend(list_of_zero_tiles)
        new_tiles_to_make_visible.extend(list_of_non_zero_tiles)
        
        self.update_visible_board(new_tiles_to_make_visible)
        self.calculate_player_board_tiles()

        #print("self.bomb_board:",self.bomb_board)
        #print("self.info_board:",self.info_board)
        #print("self.visible_board:",self.visible_board)
        #print("self.player_board:",self.player_board)

        return False
    
    def get_adjacent_non_zero_tiles(self, list_of_zero_tiles: list) -> list:
        list_of_non_zero_tiles = []
        for zero_tile_pos in list_of_zero_tiles:
            for direction in self.SURROUNDING_COORDINATES[:]:
                possible_x, possible_y = zero_tile_pos[0]-direction[0], zero_tile_pos[1]-direction[1]

                if possible_x < 0 or possible_y < 0:
                    continue

                try: 
                    if self.info_board[possible_x][possible_y] > 0:
                        list_of_non_zero_tiles.append((possible_x,possible_y))
                except IndexError:
                    pass
        return list_of_non_zero_tiles

    def get_adjacent_zero_tiles(self, orig_tile_pos: tuple, tiles_already_found=[]) -> list:
        list_of_zero_tiles = []
        #print("get_adjacent_zero_tiles ran once")
        for direction in self.SURROUNDING_COORDINATES[:4]:
            curr_tile_pos = (orig_tile_pos[0]-direction[0],orig_tile_pos[1]-direction[1])

            if curr_tile_pos[0] < 0 or curr_tile_pos[1] < 0:
                continue

            if curr_tile_pos in tiles_already_found:
                continue

            try:
                if self.info_board[curr_tile_pos[0]][curr_tile_pos[1]] == 0:
                    list_of_zero_tiles.append(curr_tile_pos)
                    tiles_already_found.append(curr_tile_pos)
                    list_of_zero_tiles.extend(self.get_adjacent_zero_tiles(curr_tile_pos,tiles_already_found))
            except IndexError:
                pass
        return list_of_zero_tiles

    def update_visible_board(self, new_tiles_to_make_visible):
        for tile_pos in new_tiles_to_make_visible:
            self.visible_board[tile_pos[0]][tile_pos[1]] = self.OPEN

    def count_total_closed_tiles(self) -> int:
        total_closed_tiles = 0
        for row in range(self.board_size):
            for column in range(self.board_size):
                if self.visible_board[row][column] == self.CLOSED:
                    total_closed_tiles += 1
        return total_closed_tiles

    def display_formatted_player_board(self):
        print("\n"*20)
        for row in self.player_board:
            for item in row:
                print(item,"", end="")
            print()

    def start_game(self):
        self.create_board()

        while self.count_total_closed_tiles() > self.bomb_count:
            if self.select_square((int(input("Please provide an x coordinate for your guess: ")), int(input("Please provide a y coordinate for your guess: ")))):
                print("You lose!")
                return
            self.display_formatted_player_board()
        print("You win!")