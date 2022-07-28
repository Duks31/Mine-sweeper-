import random
import re


# lets Create a new board object to represent the game, making it easier to create new board 
# or finding a place to dig or render the game for the object 

class Board:
    def __init__(self, dim_size, num_bombs):
        # helpful parameters
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        self.board = self.make_new_board() # plant the bombs 
        self.assign_values_to_board()

        # initialize a set to keep track of which location we've uncovered, we will save (row,col) tuples
        # into the set 
        self.dug = set() # if we dig at 0,0 , then self.dug = {(0,0)}

    def make_new_board(self):
        # Construct a new board on the dim size and new bombs 
        # Construct the list of list too , since using a 2-D board 
        
        # Generate a new board 
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this creates an array that looks something like:
        # [[None, None, ..., None],
        # [None, None, ..., None],
        # [None, None, ..., None],
        # [None, None, ..., None],
        # [None, None, ..., None]] 

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1) # return a random integer N such that a <= N <= b Where b is the max index in the list
            row = loc // self.dim_size # Num of times dim_size goes into loc to tell us the row we are looing at 
            col = loc % self.dim_size # Remainder to tell us what index in that row 

            if board[row][col]  == '*':
                # Bomb already there, Keep going 
                continue
            
            board[row][col] = '*'#plant the bomb
            bombs_planted += 1

        return board 
            
    def assign_values_to_board(self):
        # Now we have teh bombs planted, lets assign a number 0-8 for all the empty
        # representing how many negihbouring bombs there are. We can precompute this and it will be saving effort checking what's around later on
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
         # lets iterate through each of the neighboring positons and sum up the number of bombs
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # Dig that location
        # Return True if successful dig, False if bomb Dug

        # Hit  a Bomb, Game Over
        # Dig a location with Neighboring bombs -> finish dig
        # dig at location with no neighboring bombs -> recursively dig neighbours

        self.dug.add((row, col)) # keep track that we dug here 

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r,c)

        return True

    def __str__(self):
        # This is a magic function where if you call print on this object
        # It will print out what this function returns
        # return a string that shows the board to the player 

        # first lets create a new array that represents what the user would see 
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
    
        # put the entire board rep. in a string 
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep



# play the game

def play(dim_size = 10, num_bombs = 10):
    # step1: Create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # step2: Show the uset the board and ask for where they want to dig 
    # step3a: If the location is a bomb, show the game over message, Quit
    # step3b: If location is not a bomb, dig recursively unitl each square is at least next to a bomb
    # step4: Repeat step2 and step3a&b until there are no more places to dig -> Victory 
    
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)

        user_input = re.split(',(\\s)*',input('Where would you like to dig? Input as row, col: ')) # 0, 3
        row, col  = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print('Invalid Location')
            continue
        
        # if it's valid, we dig 
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb 
            break
    
    # 2 ways to end loop, lets check which one
    if safe: 
        print('Congratulatons!!! ')
    else:
        print('Sorry,  Game Over')

        # Reveal the whole board 
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__': # good practice
    play()