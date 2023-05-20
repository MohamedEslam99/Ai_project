import numpy as np
import random
import pygame
import sys
import math
import time
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

BLUE = (26, 26, 255)
WHITE = (244, 240, 224)
RED = (213, 46, 48)
YELLOW = (252, 238, 33)
BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 0, 179)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 99, 71)
LIGHT_YELLOW = (255, 255, 153)
LIGHT_GRAY = (211, 211, 211)
DARK_BLUE = (23, 42, 58)
DARK_GREEN = (30, 70, 32)
DARK_RED = (124, 10, 2)
W = (119, 117, 117, 0.584)

Rows_Count = 6  # Number of rows in the game board
Columns_Count = 7  # Number of columns in the game board
Limit = Columns_Count // 2  # Limit for column selection

Computer = 0  # Identifier for the computer player
Agent = 1  # Identifier for the agent player

EMPTY = 0  # Value representing an empty cell on the game board
ComputerPiece = 1  # Value representing a cell occupied by the computer player's piece
Agent_Piece = 2  # Value representing a cell occupied by the agent player's piece

Connect = 4  # Number of pieces required to connect for a win
Max = 100000000000000  # Maximum value used in the minimax algorithm
Min = -100000000000000  # Minimum value used in the minimax algorithm

depths = [1, 2, 3, 4, 5, 6]  # List of depths for evaluating performance
minimaxExecutionTimes = []  # List to store execution times for the minimax algorithm
alpha_beta_ExecutionTimes = []  # List to store execution times for the alpha-beta pruning algorithm

level_depths = {"Easy": 2, "Medium": 4, "Hard": 6}  # Dictionary mapping difficulty levels to corresponding depths
algorithm = {"Minimax": 1, "Alpha_beta": 2}  # Dictionary mapping algorithm names to corresponding identifiers

# Define the size of the board and margins for Macbook
BoardSize = 75  # Adjust the board size according to your preference
LeftMargin = 30  # Adjust the left margin according to your preference
RightMargin = 30  # Adjust the right margin according to your preference
TopMargin = 30  # Adjust the top margin according to your preference
BottomMargin = 30  # Adjust the bottom margin according to your preference

# Calculate the adjusted size of the screen
Width = Columns_Count * BoardSize + LeftMargin + RightMargin
Height = (Rows_Count + 1) * BoardSize + TopMargin + BottomMargin

# Calculate the adjusted size of the board
AdjustedWidth = Columns_Count * BoardSize
AdjustedHeight = Rows_Count * BoardSize

# Calculate the adjusted radius
Radius = int(BoardSize / 2 - 5)

# Create the screen with the adjusted size
screen = pygame.display.set_mode((Width, Height))

# Load background image
background_image = pygame.image.load("connect_4.jpeg")


# function creates a 6x7 grid for the game board and initializes it with zeros.
def initializeBoard():
    board = np.zeros((Rows_Count, Columns_Count))
    return board


# function updates the board with a player's move at a specified row and column.
def make_Move(board, row, col, piece):
    board[row][col] = piece  # It assigns the specified piece value to the corresponding position on the board.


# function checks if a move is valid by verifying if the bottom row of a column is empty.
def is_Move_Valid(board, col):
    return board[Rows_Count - 1][
               col] == 0  # It returns True if the move is valid (the bottom row is empty) and False otherwise.


# function returns the row where a piece will be placed based on the current column.
def getChildren(board, col):
    for row in range(Rows_Count):
        if board[row][col] == 0:
            return row


# function prints the current state of the game board.
def show_Board(board):
    print(np.flip(board, 0))


'''function checks if a player has won the game by checking 
for four consecutive pieces in horizontal, vertical, and diagonal directions.'''


def winning(board, piece):
    # Check horizontal locations for winer
    for col in range(Columns_Count - Limit):
        for row in range(Rows_Count):
            if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and \
                    board[row][
                        col + Limit] == piece:
                return True

    # Check vertical locations for winer
    for col in range(Columns_Count):
        for row in range(Rows_Count - Limit):
            if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and \
                    board[row + Limit][
                        col] == piece:
                return True

    # Check right diaganols
    for col in range(Columns_Count - Limit):
        for row in range(Rows_Count - Limit):
            if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and \
                    board[row + Limit][
                        col + Limit] == piece:
                return True

    # Check left diaganols
    for col in range(Columns_Count - Limit):
        for row in range(Limit, Rows_Count):
            if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and \
                    board[row - Limit][
                        col + Limit] == piece:
                return True


'''function calculates the score for a window of four pieces 
based on the player's piece and the number of empty spaces.'''


def calcScore(window, piece):
    score = 0
    opponent = ComputerPiece

    # Determine the opponent's piece based on the current player's piece
    if piece == ComputerPiece:
        opponent = Agent_Piece

    # Evaluate the score based on the contents of the window
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


# function evaluates the score of the current board state for a given player.
def state(board, piece):
    score = 0
    # Score center column
    centerArr = [int(i) for i in list(board[:, Limit])]
    centerCount = centerArr.count(piece)
    score += centerCount * 3

    # Score Horizontal
    for row in range(Rows_Count):
        rowArr = [int(i) for i in list(board[row, :])]
        for col in range(Columns_Count - Limit):
            window = rowArr[col:col + Connect]
            score += calcScore(window, piece)

    # Score Vertical
    for col in range(Columns_Count):
        colArr = [int(i) for i in list(board[:, col])]
        for row in range(Rows_Count - Limit):
            window = colArr[row:row + Connect]
            score += calcScore(window, piece)

    # Score right diagonal
    for row in range(Rows_Count - Limit):
        for col in range(Columns_Count - Limit):
            window = [board[row + i][col + i] for i in range(Connect)]
            score += calcScore(window, piece)

    # Score left diagonal
    for row in range(Rows_Count - Limit):
        for col in range(Columns_Count - Limit):
            window = [board[row + Limit - i][col + i] for i in range(Connect)]
            score += calcScore(window, piece)

    return score


# function checks if the game has reached a terminal state (no more valid moves or a player has won).
def isTerminalNode(board):
    # Check if there are no valid locations left on the board
    if len(getValidLocations(board)) == 0:
        return True

    # Check if either the computer or the agent has won the game
    if winning(board, ComputerPiece) or winning(board, Agent_Piece):
        return True

    # If none of the above conditions are met, the game is not yet over
    return False


# function implements the alpha-beta pruning algorithm to determine the best move for the AI player.
def alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    # Check if the current node is a terminal node or if the maximum depth is reached
    isTerminal = isTerminalNode(board)
    validLocations = getValidLocations(board)
    if depth == 0 or isTerminal:
        if isTerminal:
            # Check if the game is won by the agent or the computer
            if winning(board, Agent_Piece):
                return (Max, None)
            elif winning(board, ComputerPiece):
                return (Min, None)
            else:  # Game is over, no more valid moves
                return (0, None)
        else:  # Depth is zero
            # Evaluate the state of the board for the agent
            return (state(board, Agent_Piece), None)

    if maximizingPlayer:
        # Maximize the score for the agent
        value = -math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getChildren(board, col)
            bCopy = board.copy()
            make_Move(bCopy, row, col, Agent_Piece)
            new_score = alpha_beta(bCopy, depth - 1, alpha, beta, False)[0]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, column

    else:  # Minimizing player
        # Minimize the score for the computer
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getChildren(board, col)
            bCopy = board.copy()
            make_Move(bCopy, row, col, ComputerPiece)
            new_score = alpha_beta(bCopy, depth - 1, alpha, beta, True)[0]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, column


# function implements the minimax algorithm to determine the best move for the AI player.
def minimax(board, depth, maximizingPlayer):
    # Check if the current node is a terminal node or if the maximum depth is reached
    isTerminal = isTerminalNode(board)
    validLocations = getValidLocations(board)
    if depth == 0 or isTerminal:
        if isTerminal:
            # Check if the game is won by the agent or the computer
            if winning(board, Agent_Piece):
                return (Max, None)
            elif winning(board, ComputerPiece):
                return (Min, None)
            else:  # Game is over, no more valid moves
                return (0, None)
        else:  # Depth is zero
            # Evaluate the state of the board for the agent
            return (state(board, Agent_Piece), None)

    if maximizingPlayer:
        # Maximize the score for the agent
        value = -math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getChildren(board, col)
            bCopy = board.copy()
            make_Move(bCopy, row, col, Agent_Piece)
            new_score = minimax(bCopy, depth - 1, False)[0]
            if new_score > value:
                value = new_score
                column = col
        return value, column

    else:  # Minimizing player
        # Minimize the score for the computer
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            row = getChildren(board, col)
            bCopy = board.copy()
            make_Move(bCopy, row, col, ComputerPiece)
            new_score = minimax(bCopy, depth - 1, True)[0]
            if new_score < value:
                value = new_score
                column = col
        return value, column


# function returns a list of valid column indices where a piece can be placed.
def getValidLocations(board):
    # Create a list to store valid column locations
    valid_locations = []

    # Iterate over each column in the board
    for col in range(Columns_Count):
        # Check if the move is valid for the current column
        if is_Move_Valid(board, col):
            # If the move is valid, add the column to the list of valid locations
            valid_locations.append(col)

    # Return the list of valid column locations
    return valid_locations


# function selects the best move for the AI player based on the current board state and the player's piece.
def bestMove(board, piece):
    # Get valid locations where the piece can be placed
    validLocations = getValidLocations(board)

    # Initialize the best score with a low value
    bestScore = -10000

    # Initialize the best column with a random choice from valid locations
    bestCol = random.choice(validLocations)

    # Iterate over each valid column and evaluate the potential moves
    for col in validLocations:
        # Get the corresponding row for the current column
        row = getChildren(board, col)

        # Create a copy of the board to simulate the move
        TBoard = board.copy()

        # Make the move on the temporary board
        make_Move(TBoard, row, col, piece)

        # Evaluate the score for the current move
        score = state(TBoard, piece)

        # Update the best score and best column if the current score is better
        if score > bestScore:
            bestScore = score
            bestCol = col

    # Return the best column to make the move
    return bestCol


# function updates the game interface to display the current state of the board.
def drawBoard(board):
    for col in range(Columns_Count):
        for row in range(Rows_Count):
            pygame.draw.rect(screen, LIGHT_YELLOW, (
                LeftMargin + col * BoardSize, TopMargin + row * BoardSize + BoardSize, BoardSize, BoardSize))
            pygame.draw.circle(screen, LIGHT_GRAY, (
                int(LeftMargin + col * BoardSize + BoardSize / 2),
                int(TopMargin + row * BoardSize + BoardSize + BoardSize / 2)), Radius)

    for col in range(Columns_Count):
        for row in range(Rows_Count):
            if board[row][col] == ComputerPiece:
                pygame.draw.circle(screen, LIGHT_RED, (
                    int(LeftMargin + col * BoardSize + BoardSize / 2),
                    Height - int(TopMargin + row * BoardSize + BoardSize / 2)), Radius)
            elif board[row][col] == Agent_Piece:
                pygame.draw.circle(screen, LIGHT_BLUE, (
                    int(LeftMargin + col * BoardSize + BoardSize / 2),
                    Height - int(TopMargin + row * BoardSize + BoardSize / 2)), Radius)
    pygame.display.update()


''' function generates a performance graph comparing 
the execution times of the minimax and alpha-beta algorithms for different depths.'''


def Drawgraph():
    # Iterate over the depths to evaluate the performance for each depth
    for Depth in depths:
        # Measure the execution time for the minimax algorithm
        start_time = time.time()
        minimax(B, Depth, True)
        end_time = time.time()
        minimaxExecutionTimes.append(end_time - start_time)

        # Measure the execution time for the alpha-beta pruning algorithm
        start_time = time.time()
        alpha_beta(B, Depth, -math.inf, math.inf, True)
        end_time = time.time()
        alpha_beta_ExecutionTimes.append(end_time - start_time)

    # Create the performance graph
    plt.plot(depths, minimaxExecutionTimes, label='Minimax')
    plt.plot(depths, alpha_beta_ExecutionTimes, label='Alpha-Beta pruning')
    plt.title('The Performance of the Two Algorithms: Minimax vs Alpha-Beta')
    plt.xlabel('Depth')
    plt.ylabel('Time in Seconds')
    plt.legend()

    # Save the performance graph as an image file
    plt.savefig('performance.jpg')


board = initializeBoard()
B = board
