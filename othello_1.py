import sys
import time

state = "...........................ox......xo..........................."
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
eight_x_eight = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88]
corners = {
    0:{1, 8, 9},
    7:{6, 15, 14}, 
    56: {57, 48, 49},
    63: {62, 55, 54}}
char_to_val = {"x":1, "o":-1, ".": 0}

def make_100_char(board):
    new_board = "???????????"
    for line in range(8):
        row = line * 8
        new_board += board[row: row + 8]
        new_board += "??"
    new_board += "?????????"
    new_board = list(new_board)
    return new_board

def make_64_char(board):
 #   newboard = [token for index, token in enumerate(board[11:89]) if index % 10 < 8 ]
    newboard = [board[index] for index in eight_x_eight]
    return "".join(newboard)


def ten_to_eight(index):
   row = index//10
   index = index - 2*row -9
   return index

def eight_to_ten(index):
    return (index//8 +1) * 10 + (index% 8 + 1)

def display_board(board):
    s = ""
    side = int(len(board)**0.5)
    for ind1 in range(side):
        for ind2 in range(side):
            s += board[ind1 * side + ind2]
            s += " "
        s += "\n"
    return s

def possible_moves(board, token):
    board = make_100_char(board)
    opp = "ox"["xo".index(token)]
    moves = set()
    token_spots = [index for index, val in enumerate(board) if val == token]
    for spot in token_spots:
        for direction in directions:
            next_index = spot + direction
            while board[next_index] == opp:
                next_index += direction
                if board[next_index] == ".":
                    moves.add(ten_to_eight(next_index))

    converted = []
    for i in moves:
        converted.append(i)
    return converted

def make_move(board, token, index):
    board = make_100_char(board)
    index = eight_to_ten(index)
    board[index] = token
    opp = "ox"["xo".index(token)]
    for direction in directions:
        next_index = index + direction
        changes = set()
        while board[next_index] == opp:
            changes.add(next_index)
            next_index = next_index + direction
        if board[next_index] == token:
            for change in changes:
                board[change] = token
    return make_64_char(board)

def score(board, x_moves, o_moves):
    score = 0
    if len(x_moves) == 0 and len(o_moves) == 0:
        return 1000 * board.count("x") - board.count("o")
    for c in corners:
        for neighbor in corners[c]:
            score -= 10 * char_to_val[board[neighbor]]
        score += 100 * char_to_val[board[c]]
    return score + len(x_moves) - len(o_moves)

def max_step(board, depth):
    possible = possible_moves(board, "x")
    possible_o = possible_moves(board, "o")
    if depth == 0 or (len(possible) == 0 and len(possible_o) == 0):
        return score(board, possible, possible_o)
    elif len(possible) == 0:
        return min_step(board, depth)
    else:
        moves = [make_move(board, "x", index) for index in possible]
        return max([min_step(move, depth-1) for move in moves])

def min_step(board, depth):
    possible = possible_moves(board, "o")
    possible_x = possible_moves(board, "x")
    if depth == 0 or (len(possible_x) == 0 and  len(possible) == 0):
        return score(board, possible_x, possible)
    elif len(possible) == 0:
        return max_step(board, depth)
    else:
        moves = [make_move(board, "o", index) for index in possible]
        return min([max_step(move, depth-1) for move in moves])


def find_next_move(board, player, depth):
    if player == "x":
        move_list = possible_moves(board, player)
        scores = [min_step(make_move(board, "x", move), depth) for move in move_list]
        move_index = scores.index(max(scores))
        return move_list[move_index]
    else:
        move_list = possible_moves(board, player)
        scores = [max_step(make_move(board, "o", move), depth) for move in move_list]
        move_index = scores.index(min(scores))
        return move_list[move_index]
        

# results = []
# with open("boards_timing.txt") as f:
#     for line in f:
#         board, token = line.strip().split()
#         temp_list = [board, token]
#         print(temp_list)
#         for count in range(1, 6):
#             print("depth", count)
#             start = time.perf_counter()
#             find_next_move(board, token, count)
#             end = time.perf_counter()
#             temp_list.append(str(end - start))
#         print(temp_list)
#         print()
#         results.append(temp_list)

# with open("boards_timing_my_results.csv", "w") as g:
#     for l in results:
#         g.write(", ".join(l) + "\n")

board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1

# class Strategy():
#    logging = True  # Optional
#    def best_strategy(self, board, player, best_move, still_running):
#        depth = 1
#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

#            best_move.value = find_next_move(board, player, depth)

#            depth += 1