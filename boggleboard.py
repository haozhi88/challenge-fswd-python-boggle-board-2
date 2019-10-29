"""""""""""""""""""""
Import libraries
"""""""""""""""""""""
import random

"""""""""""""""""""""
Constant variables
"""""""""""""""""""""
DEFAULT_DICE = [
    ['A','A','E','E','G','N'],  # 0
    ['E','L','R','T','T','Y'],  # 1
    ['A','O','O','T','T','W'],  # 2
    ['A','B','B','J','O','O'],  # 3
    ['E','H','R','T','V','W'],  # 4
    ['C','I','M','O','T','U'],  # 5
    ['D','I','S','T','T','Y'],  # 6
    ['E','I','O','S','S','T'],  # 7
    ['D','E','L','R','V','Y'],  # 8
    ['A','C','H','O','P','S'],  # 9
    # ['H','I','M','N','Qu','U'], # 10
    ['H','I','M','N','Q','U'], # 10
    ['E','E','I','N','S','U'],  # 11
    ['E','E','G','H','N','W'],  # 12
    ['A','F','F','K','P','S'],  # 13
    ['H','L','N','N','R','Z'],  # 14
    ['D','E','I','L','R','X']   # 15
]
TOTAL_DICES = 16

"""""""""""""""""""""
Global variables
"""""""""""""""""""""
board = [
    ["","","",""],
    ["","","",""],
    ["","","",""],
    ["","","",""]
    ]
stack = []
word = ""

"""""""""""""""""""""
Functions
"""""""""""""""""""""
def get_random_board():
    global board
    check = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i,i_item in enumerate(board):
        for j,j_item in enumerate(board[i]):
            while True:
                index = random.randint(0,TOTAL_DICES-1)
                if check[index] == 0:
                    board[i][j] = random.choice(DEFAULT_DICE[index])
                    check[index] = 1
                    break

def display_board():
    string = "\n"
    string += "------------\n"
    string += "Boggle Board\n"
    string += "------------\n"
    for i,i_item in enumerate(board):
        for j,j_item in enumerate(board[i]):
            string += j_item.ljust(3)
        string += "\n"
    string += "------------\n"
    print(string)

def display_word():
    string = "------------------------\n"
    string += f"Word entered: {word}\n"
    string += "------------------------\n"
    print(string)

def get_input():
    global word
    while True:
        print("0: Quit")
        print("1: Shuffle board")
        print("Others: Enter a word")
        userinput = input("Type: ")

        if userinput == "0":
            return 0 # quit
        elif userinput == "1":
            return 1 # shuffle board
        elif len(userinput) < 3:
            print("[Alert] Please enter >= 3 characters.")
        elif not userinput.isalpha():
            print("[Alert] Please enter only alphabets.")
        else:
            word = userinput.upper()
            return 2 # play game

def display_result():
    string = "\n"
    string += "------------\n"
    string += f"Result: {check_word()}\n"
    string += "------------\n"
    print(string)


"""""""""""""""""""""""""""""""""""""""""
Pos[0,1] = [vertical-y, horizontal-x]
"""""""""""""""""""""""""""""""""""""""""
def clear_stack():
    global stack
    stack = []

def push_stack(pos):
    global stack
    if len(stack) < 2:
        stack.append(pos)
    else:
        if stack[-2] == pos:
            # avoid matching same position
            return False
        else:
            stack.append(pos)
    return True

def pop_stack():
    global stack
    if len(stack) == 0:
        print("[ERROR]: pop_trace")
    else:
        stack.pop()

def check_word():
    index = 0
    pos = find_first_char(word[index])
    for i, i_item in enumerate(pos):
        clear_stack()
        if push_stack(i_item):            
            if find_next_char(index, i_item):
                # print(f"stack: {stack}")
                return True
    return False

def find_first_char(char):
    count = 0
    pos = []
    for i,i_item in enumerate(board):
        for j,j_item in enumerate(board[i]):
            if j_item == char:
                pos.append([i,j])
                count += 1
    return pos

def find_next_char(index, pos):
    if index + 1 == len(word):
        return True
    else:
        next_pos = []
        next_pos.extend(find_horizontal(index, pos))
        next_pos.extend(find_vertical(index, pos))
        next_pos.extend(find_diagonal(index, pos))
        if len(next_pos) == 0:
            return False
        else:
            for i,i_item in enumerate(next_pos):
                if push_stack(i_item):                
                    if find_next_char(index+1, i_item):
                        return True
                    else:
                        pop_stack()        
    return False

def find_horizontal(index, pos):
    next_pos = []

    if index + 1 == len(word):
        return next_pos
    else:
        x = pos[1] # horizontal along x-axis
        y = pos[0]
        left_x = x-1
        right_x = (x+1)%4
        next_char = word[index+1]

        if board[y][left_x] == next_char:
            next_pos.append([y, left_x])
        if board[y][right_x] == next_char:
            next_pos.append([y, right_x])
    return next_pos

def find_vertical(index, pos):
    next_pos = []

    if index + 1 == len(word):
        return next_pos
    else:
        x = pos[1] 
        y = pos[0] # vertical along y-axis
        upper_y = y-1
        lower_y = (y+1)%4
        next_char = word[index+1]

        if board[upper_y][x] == next_char:
            next_pos.append([upper_y, x])
        if board[lower_y][x] == next_char:
            next_pos.append([lower_y, x])
    return next_pos

def find_diagonal(index, pos):
    next_pos = []

    if index + 1 == len(word):
        return next_pos
    else:
        x = pos[1] # horizontal along x-axis
        y = pos[0] # vertical along y-axis
        left_x = x-1
        right_x = (x+1)%4
        upper_y = y-1
        lower_y = (y+1)%4
        next_char = word[index+1]

        if board[upper_y][left_x] == next_char:
            next_pos.append([upper_y, left_x])
        if board[upper_y][right_x] == next_char:
            next_pos.append([upper_y, right_x])
        if board[lower_y][left_x] == next_char:
            next_pos.append([lower_y, left_x])
        if board[lower_y][right_x] == next_char:
            next_pos.append([lower_y, right_x])
    return next_pos

"""""""""""""""""""""
Main Program
"""""""""""""""""""""
while True:
    get_random_board()
    display_board()
    result = get_input()
    if result == 0:
        break
    elif result == 1:
        continue
    elif result == 2:
        display_word()
        display_result()
    else:
        print("[ERROR]: Main program")
        break



