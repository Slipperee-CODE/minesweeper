import random

class Minesweeper():
    def __init__(self, board_size: int, bomb_count: int):
        self.board_size = board_size
        self.bomb_count = bomb_count
        self.bomb_board = []
        self.info_board = []
        self.visible_board = []
        self.player_board = []
        self.OPEN = "[O]"
        self.CLOSED = "[ ]"
        self.SURROUNDING_COORDINATES = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,-1), (-1,1)]
    
    def create_board(self):
        self.bomb_board = [[0 for i in range(self.board_size)] for i in range(self.board_size)]
        self.info_board = [[0 for i in range(self.board_size)] for i in range(self.board_size)]
        self.visible_board = [[self.CLOSED for i in range(self.board_size)] for i in range(self.board_size)]
        self.player_board = [[self.CLOSED for i in range(self.board_size)] for i in range(self.board_size)]

        bomb_positions = []
        while len(bomb_positions) < self.bomb_count:
            curr_bomb_pos = (random.randint(0, self.board_size-1), random.randint(0, self.board_size-1))
            if curr_bomb_pos not in bomb_positions:
                bomb_positions.append(curr_bomb_pos)

        for bomb_pos in bomb_positions:
            self.bomb_board[bomb_pos[0]][bomb_pos[1]] == 1

        self.calculate_info_board_tiles()
    
    def calculate_info_board_tiles(self):
        for row in self.info_board:
            for column in row:
                sum_of_tile_surroundings = self.calculate_tile_surroundings((row, column))
                self.info_board[row][column] = sum_of_tile_surroundings

    def calculate_player_board_tiles(self):
        for row in self.visible_board:
            for column in row:
                if self.visible_board[row][column] == self.OPEN:
                    self.player_board[row][column] = self.info_board[row][column]

    def select_square(self, pos: tuple) -> bool:
        if (self.bomb_board[pos[0]][pos[1]]):
            return True
        self.visible_board[pos[0]][pos[1]] = self.OPEN
        new_tiles_to_make_visible = self.get_adjacent_zero_tiles()
        self.update_visible_board(new_tiles_to_make_visible)
        self.calculate_player_board_tiles()
        return False

    def calculate_tile_surroundings(self, pos: tuple) -> int:
        sum = 0
        for direction in self.SURROUNDING_COORDINATES:
            try:
                sum += self.board[pos[0]-direction[0]][pos[1]-direction[1]]
            except:
                pass
        return sum
    
    def get_adjacent_zero_tiles(self, orig_tile_pos) -> list:
        list_of_zero_tiles = []
        for direction in self.SURROUNDING_COORDINATES:
            try:
                possible_x = orig_tile_pos[0]-direction[0]
                possible_y = orig_tile_pos[1]-direction[1]
                if self.info_board[possible_x][possible_y] == 0:
                    list_of_zero_tiles.append((possible_x,possible_y))
                    list_of_zero_tiles.extend(self.get_adjacent_zero_tiles((possible_x,possible_y)))
            except:
                pass
        return list_of_zero_tiles

    def update_visible_board(self, new_tiles_to_make_visible):
        for tile_pos in new_tiles_to_make_visible:
            self.visible_board[tile_pos[0]][tile_pos[1]] = self.OPEN

    def start_game(self):
        self.create_board()
        while self.visible_board.count(self.CLOSED) > self.bomb_count:
            if self.select_square((input("Please provide an x coordinate for your guess: "), input("Please provide a y coordinate for your guess: "))):
                print("You lose!")
                break
            print(self.player_board)
        print("You win!")