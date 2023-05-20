from Board import *

show_Board(board)  # Display the initial board
game_over = False


# Function to display the algorithm selection menu
def show_Algorithm():
    screen.fill(WHITE)
    global Selected_Algo, A
    menuFont = pygame.font.SysFont("Open Sans", 50)
    title = menuFont.render("Connect-4", 1, BLUE)
    screen.blit(title, (Width / 2 - title.get_width() / 2, 50))

    # Define button dimensions
    buttonWidth = 200
    buttonHeight = 50

    # Create Minimax button
    MinimaxButtonRect = pygame.Rect((Width - buttonWidth) / 2, 300, buttonWidth, buttonHeight)
    MinimaxButtonColor = BLUE
    pygame.draw.rect(screen, MinimaxButtonColor, MinimaxButtonRect)
    Minimax = menuFont.render("Minimax", 1, WHITE)
    screen.blit(Minimax, (
        MinimaxButtonRect.centerx - Minimax.get_width() / 2,
        MinimaxButtonRect.centery - Minimax.get_height() / 2))

    # Create Alpha_beta button
    Alpha_betaButtonRect = pygame.Rect((Width - buttonWidth) / 2, 200, buttonWidth, buttonHeight)
    Alpha_betaButtonColor = BLUE
    pygame.draw.rect(screen, Alpha_betaButtonColor, Alpha_betaButtonRect)
    Alpha_beta = menuFont.render("Alpha_beta", 1, WHITE)
    screen.blit(Alpha_beta,
                (Alpha_betaButtonRect.centerx - Alpha_beta.get_width() / 2,
                 Alpha_betaButtonRect.centery - Alpha_beta.get_height() / 2))

    # Blit background image
    screen.blit(background_image, (0, 0))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if MinimaxButtonRect.collidepoint(pos):
                    Selected_Algo = "Minimax"
                    A = algorithm[Selected_Algo]
                    return
                elif Alpha_betaButtonRect.collidepoint(pos):
                    Selected_Algo = "Alpha_beta"
                    A = algorithm[Selected_Algo]
                    return

            elif event.type == pygame.MOUSEMOTION:
                # Check if mouse is hovering over the buttons
                if MinimaxButtonRect.collidepoint(event.pos):
                    MinimaxButtonColor = LIGHT_BLUE
                else:
                    MinimaxButtonColor = BLUE
                if Alpha_betaButtonRect.collidepoint(event.pos):
                    Alpha_betaButtonColor = LIGHT_BLUE
                else:
                    Alpha_betaButtonColor = BLUE

        pygame.draw.rect(screen, MinimaxButtonColor, MinimaxButtonRect)
        screen.blit(Minimax, (
            MinimaxButtonRect.centerx - Minimax.get_width() / 2, MinimaxButtonRect.centery - Minimax.get_height() / 2))
        pygame.draw.rect(screen, Alpha_betaButtonColor, Alpha_betaButtonRect)
        screen.blit(Alpha_beta,
                    (Alpha_betaButtonRect.centerx - Alpha_beta.get_width() / 2,
                     Alpha_betaButtonRect.centery - Alpha_beta.get_height() / 2))

        pygame.display.update()


# Function to display the difficulty level selection menu
def show_Levels():
    screen.fill(WHITE)
    global Selected_level, Level
    menuFont = pygame.font.SysFont("Open Sans", 50)
    title = menuFont.render(Selected_Algo + " algorithm", 1, DARK_BLUE)
    screen.blit(title, (Width / 2 - title.get_width() / 2, 50))

    # Define button dimensions
    buttonWidth = 200
    buttonHeight = 50

    # Create Easy button
    easyButtonRect = pygame.Rect((Width - buttonWidth) / 2, 200, buttonWidth, buttonHeight)
    easyButtonColor = DARK_BLUE
    pygame.draw.rect(screen, easyButtonColor, easyButtonRect)
    easy = menuFont.render("Easy", 1, WHITE)
    screen.blit(easy, (easyButtonRect.centerx - easy.get_width() / 2, easyButtonRect.centery - easy.get_height() / 2))

    # Create Medium button
    mediumButtonRect = pygame.Rect((Width - buttonWidth) / 2, 300, buttonWidth, buttonHeight)
    mediumButtonColor = DARK_GREEN
    pygame.draw.rect(screen, mediumButtonColor, mediumButtonRect)
    medium = menuFont.render("Medium", 1, WHITE)
    screen.blit(medium,
                (mediumButtonRect.centerx - medium.get_width() / 2, mediumButtonRect.centery - medium.get_height() / 2))

    # Create Hard button
    hardButtonRect = pygame.Rect((Width - buttonWidth) / 2, 400, buttonWidth, buttonHeight)
    hardButtonColor = DARK_RED
    pygame.draw.rect(screen, hardButtonColor, hardButtonRect)
    hard = menuFont.render("Hard", 1, WHITE)
    screen.blit(hard, (hardButtonRect.centerx - hard.get_width() / 2, hardButtonRect.centery - hard.get_height() / 2))

    # Blit background image
    screen.blit(background_image, (0, 0))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easyButtonRect.collidepoint(pos):
                    Selected_level = "Easy"
                    Level = level_depths[Selected_level]
                    return
                elif mediumButtonRect.collidepoint(pos):
                    Selected_level = "Medium"
                    Level = level_depths[Selected_level]
                    return
                elif hardButtonRect.collidepoint(pos):
                    Selected_level = "Hard"
                    Level = level_depths[Selected_level]
                    return
            elif event.type == pygame.MOUSEMOTION:
                # Check if mouse is hovering over the buttons
                if easyButtonRect.collidepoint(event.pos):
                    easyButtonColor = LIGHT_BLUE
                else:
                    easyButtonColor = DARK_BLUE
                if mediumButtonRect.collidepoint(event.pos):
                    mediumButtonColor = LIGHT_GREEN
                else:
                    mediumButtonColor = DARK_GREEN
                if hardButtonRect.collidepoint(event.pos):
                    hardButtonColor = LIGHT_RED
                else:
                    hardButtonColor = DARK_RED

        pygame.draw.rect(screen, easyButtonColor, easyButtonRect)
        screen.blit(easy,
                    (easyButtonRect.centerx - easy.get_width() / 2, easyButtonRect.centery - easy.get_height() / 2))
        pygame.draw.rect(screen, mediumButtonColor, mediumButtonRect)
        screen.blit(medium,
                    (mediumButtonRect.centerx - medium.get_width() / 2,
                     mediumButtonRect.centery - medium.get_height() / 2))
        pygame.draw.rect(screen, hardButtonColor, hardButtonRect)
        screen.blit(hard,
                    (hardButtonRect.centerx - hard.get_width() / 2, hardButtonRect.centery - hard.get_height() / 2))

        pygame.display.update()


# Initialize Pygame
pygame.init()

# Show the algorithm selection menu
show_Algorithm()

# Show the difficulty level selection menu
show_Levels()

# Clear the screen and draw the board
screen.fill(WHITE)
drawBoard(board)
pygame.display.update()

# Randomly determine who goes first
turn = random.randint(Computer, Agent)

# Font for displaying game results
Font = pygame.font.SysFont("Helvetica", 60)

# Start the game loop
while not game_over:

    # Computer's turn
    if turn == Computer:
        # Determine the move using the selected algorithm and level
        if A == 1:
            Score, col = minimax(board, Level, False)
        else:
            Score, col = alpha_beta(board, Level - 1, -math.inf, math.inf, False)

        # Check if the selected move is valid
        if is_Move_Valid(board, col).any():
            pygame.time.wait(420)
            row = getChildren(board, col)
            make_Move(board, row, col, ComputerPiece)

            # Check if the computer wins
            if winning(board, ComputerPiece):
                label = Font.render(" Computer wins", 1, RED)
                print("Computer wins")
                screen.blit(label, (30, 30))
                game_over = True

            # Switch turns
            turn += 1
            turn = turn % 2

            # Update the board display
            show_Board(board)
            drawBoard(board)

    # Agent's turn
    if turn == Agent and not game_over:
        # Determine the move using the selected algorithm and level
        if A == 1:
            Score, col = minimax(board, Level, True)
        else:
            Score, col = alpha_beta(board, Level, -math.inf, math.inf, True)

        # Check if the selected move is valid
        if is_Move_Valid(board, col).any():
            pygame.time.wait(200)
            row = getChildren(board, col)
            make_Move(board, row, col, Agent_Piece)

            # Check if the agent wins
            if winning(board, Agent_Piece):
                label = Font.render("Agent wins", 1, BLUE)
                print("Agent wins")
                screen.blit(label, (30, 30))
                game_over = True

            # Update the board display
            show_Board(board)
            drawBoard(board)

            # Switch turns
            turn += 1
            turn = turn % 2

    # Check if it's a tie
    if len(getValidLocations(board)) == 0:
        label = Font.render("Draw", 1, BLUE)
        game_over = True
        print("Draw")
        screen.blit(label, (30, 30))
        show_Board(board)
        drawBoard(board)

    # Pause before showing the game result
    if game_over:
        pygame.time.wait(3000)

# Draw the graph
Drawgraph()
