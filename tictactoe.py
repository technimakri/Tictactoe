import copy, random, string, sys

class Grid:

    def __init__(self):
        self.matrix = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]

    def print_grid(self):
            print("---------")
            print("| " + " ".join(self.matrix[0]) + " |")
            print("| " + " ".join(self.matrix[1]) + " |")
            print("| " + " ".join(self.matrix[2]) + " |")
            print("---------")

    def game_complete(self):
        if "_" not in [symbol for row in self.matrix for symbol in row]:
            return True
        else:
            return False

    def grid_indexes(self):
        """
        Returns a dictionary of indexes (keys) and their symbols (values) from the grid.
        """
        return {(row_index, symbol_index): symbol for row_index, row in enumerate(self.matrix)
                            for symbol_index, symbol in enumerate(row)}

    def unoccupied_indexes(self):
        return [index for index, symbol in self.grid_indexes().items() if symbol == "_"]

    def winning_lines(self):
        """
        Returns a list of dictionaries containing indexes and symbols of the winning lines
        """
        grid_dict = self.grid_indexes()
        row_0 = {(0, i): grid_dict[(0, i)] for i in range(3)}
        row_1 = {(1, i): grid_dict[(1, i)] for i in range(3)}
        row_2 = {(2, i): grid_dict[(2, i)] for i in range(3)}
        column_0 = {(i, 0): grid_dict[(i, 0)] for i in range(3)}
        column_1 = {(i, 1): grid_dict[(i, 1)] for i in range(3)}
        column_2 = {(i, 2): grid_dict[(i, 2)] for i in range(3)}
        diagonal_0 = {(i, i): grid_dict[(i, i)] for i in range(3)}
        diagonal_1 = {(i, x): grid_dict[(i, x)] for i, x in enumerate(range(2, -1, -1))}

        return [row_0, row_1, row_2, column_0, column_1, column_2, diagonal_0, diagonal_1]

    def win_condition_check(self):
        line_list = []
        for line in self.winning_lines():
            line_list.append(list(line.values()))
        if ['X', 'X', 'X'] in line_list:
            return "X"
        elif ['O', 'O', 'O'] in line_list:
            return "O"
        elif self.game_complete():
            return "Draw"
        else:
            return False

class Player:

    def __init__(self, symbol, type):
        self.symbol = symbol
        self.type = type

    def opponent(self):
        if self.symbol == "X":
            return player_o
        else:
            return player_x

    def move(self):
        if self.type == "user":
            self.user_move()
        else:
            self.comp_move()

    def user_move(self):
        while True:
            input_coord = input("Enter the coordinates: ").split()

            # Coordinate input validation
            if any(coord not in string.digits for coord in input_coord):
                print("You should enter two single numbers!")
                continue
            if len(input_coord) != 2:
                print("Only enter two coordinates!")
                continue

            int_coord = [int(coord) for coord in input_coord]
            if any(coord < 1 or coord > 3 for coord in int_coord):
                print("Coordinates should be from 1 to 3!")
                continue

            user_index = [-1 * (int_coord[1] - 3), int_coord[0] - 1] # Converts user coordinates into a matrix index.
            if playing_grid.matrix[user_index[0]][user_index[1]] != "_":
                print("This cell is occupied! Choose another one!")
                continue
            else:
                break
        playing_grid.matrix[user_index[0]][user_index[1]] = self.symbol

    def comp_move(self):
        if self.type == "easy":
            print('Making move level "easy"')
            comp_index = self.easy_comp_move()
        elif self.type == "medium":
            print('Making move level "medium"')
            comp_index = self.med_comp_move()
        elif self.type == "hard":
            print('Making move level "hard"')
            comp_index = self.hard_comp_move()
        playing_grid.matrix[comp_index[0]][comp_index[1]] = self.symbol

    def easy_comp_move(self):
        return random.choice(playing_grid.unoccupied_indexes())

    def med_comp_move(self):

        def get_first_index(val, line):
            """
            Gets the first index (key) of a given symbol (value) from the specified winning line (dictionary)
            """
            for key, value in line.items():
                if val == value:
                    return key

        def count_symbols(line, symbol):
            return list(line.values()).count(symbol)

        for line in playing_grid.winning_lines():
            if count_symbols(line, self.symbol) == 2 and count_symbols(line, "_") == 1:
                return get_first_index("_", line)
            if count_symbols(line, self.symbol) == 0 and count_symbols(line, "_") == 1:
                return get_first_index("_", line)

        return self.easy_comp_move()

    def hard_comp_move(self):
        # The best possible turn 1 move
        if turn_counter == 1:
            return (0, 0)
        else:
            best_move = self.min_max()
            return best_move["index"]

    def min_max(self, grid=None, player=None):
        if grid == None:
            grid = playing_grid
        if player == None:
            player = self

        # Base case
        if grid.win_condition_check() == self.symbol:
            return {"score": 1}
        elif grid.win_condition_check() == self.opponent().symbol:
            return {"score": -1}
        elif grid.game_complete():
            return {"score": 0}

        # Recursion
        unoccupied_list = grid.unoccupied_indexes()
        move_list = []
        for index in unoccupied_list:
            next_move_grid = copy.deepcopy(grid)
            next_move_grid.matrix[index[0]][index[1]] = player.symbol
            move_score_dict = {}
            move_score_dict["index"] = index
            result = self.min_max(next_move_grid, player.opponent())["score"]
            move_score_dict["score"] = result
            move_list.append(move_score_dict)

        # Finding best move
        if player.symbol == self.symbol:
            best_score = -1000000
            for move in move_list:
                if move["score"] > best_score:
                    best_move = move
                    best_score = move["score"]
        elif player.symbol == self.opponent().symbol:
            best_score = 1000000
            for move in move_list:
                if move["score"] < best_score:
                    best_move = move
                    best_score = move["score"]
        return best_move

command_dict = {"menu_commands": ["start", "exit"], "player_commands": ["user", "easy", "medium", "hard"]}

def game_options():
    """
    Creates the player objects through commands.
    """
    while True:
        command_list = input("Input command: ").split(" ")
        if (command_list[0] not in command_dict["menu_commands"]
                or command_list[0] == "start" and any(command not in command_dict["player_commands"] for command in command_list[1:])
                or command_list[0] == "start" and len(command_list) < 3):
            print("Bad parameters!")
            continue
        if command_list[0] == "exit":
            sys.exit()
        else:
            break

    return Player("X", command_list[1]), Player("O", command_list[2])

def print_win(condition):
    if condition == "X" or condition == "O":
        print(f"{condition} wins")
    else:
        print(condition)

playing_grid = Grid()
turn_counter = 1
player_x, player_o = game_options()
playing_grid.print_grid()

while True:
    if turn_counter % 2 == 1:
        player_x.move()
    else:
        player_o.move()
    playing_grid.print_grid()

    if playing_grid.win_condition_check():
        print_win(playing_grid.win_condition_check())
        break
    turn_counter += 1
