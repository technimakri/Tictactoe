import string
playing_grid = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
turn_counter = 1

def game_complete():
    if "_" not in [symbol for row in playing_grid for symbol in row]:
        return True
    else:
        return False

def print_grid():
    print("---------")
    print("| " + " ".join(playing_grid[0]) + " |")
    print("| " + " ".join(playing_grid[1]) + " |")
    print("| " + " ".join(playing_grid[2]) + " |")
    print("---------")

def win_condition(line):
    if set(line) == {"X"}:
        return "X"
    if set(line) == {"O"}:
        return "O"
    else:
        return False

print_grid()
while True:
    input_coord = input("Enter the coordinates: ").split()
    int_coord = [int(coord) for coord in input_coord]
    matrix_index = [-1 * (int_coord[1] - 3), int_coord[0] - 1] # Converting inputted coordinates into matrix indexes

    # Coordinate input validation
    if any(coord not in string.digits for coord in input_coord):
        print("You should enter numbers!")
        continue
    if len(input_coord) != 2:
        print("Only enter two coordinates!")
        continue
    if any(coord < 1 or coord > 3 for coord in int_coord):
        print("Coordinates should be from 1 to 3!")
        continue
    if playing_grid[matrix_index[0]][matrix_index[1]] != "_":
        print("This cell is occupied! Choose another one!")
        continue

    # Symbol replacment
    if turn_counter % 2 == 0:
        playing_grid[matrix_index[0]][matrix_index[1]] = "X" # "X" plays on even turns
        turn_counter += 1
    else:
        playing_grid[matrix_index[0]][matrix_index[1]] = "O" # "O" plays on odd
        turn_counter += 1

    print_grid()

    # Defining non-row winning lines
    column_0 = [row[0] for row in playing_grid]
    column_1 = [row[1] for row in playing_grid]
    column_2 = [row[2] for row in playing_grid]
    diagonal_0 = [row[count] for count, row in enumerate(playing_grid)]
    diagonal_1 = [row[count + (count - 1) * -2] for count, row in enumerate(playing_grid)]

    # Win condition check
    winning_lines = [playing_grid[0], playing_grid[1], playing_grid[2], column_0,
                     column_1, column_2, diagonal_0, diagonal_1]
    win_check = [win_condition(line) for line in winning_lines]
    if "X" in win_check:
        print("X wins")
        break
    elif "O" in win_check:
        print("O wins")
        break
    if game_complete():
        print("Draw")
        break
