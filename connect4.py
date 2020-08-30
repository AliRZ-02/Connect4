'''
Name: Ali Raza Zaidi
Project: Connect4 - Complete 2020 Python Bootcamp Milestone Project 2
Description: Connect4 game vs computer or against another person
Github Repository: https://github.com/AliRZ-02/Connect4
Creation Date: 08/27/2020
Last Modified: 08/29/2020
'''

from random import randint, shuffle

def start_game():
    '''
    This function is called at the beginning of every new game - it sets the board and takes the players' names
    and returns them.
    '''
    playerNames = []
    print("Welcome to Connect4! To play against a computer, type '0'; To play against a friend, type '1'")
    while True:
        try:
            opponent = int(input(""))
            if opponent == 0 or opponent == 1:
                mode = opponent
                break
            else:
                print("An error ocurred. Please type '0' to play against a computer or '1' to play against a friend")
                pass
        except:
            print("An error ocurred. Please type '0' to play against a computer or '1' to play against a friend")
    if opponent == 0:
        playerNames.append(input("Please enter your name: "))
    else:
        for i in range(0, 2):
            playerNames.append(input("Please enter the name of player {}: ".format(i + 1)))
    return playerNames, mode

def check_win(current_board):
    '''
    This function checks to see whether or not the game has been won yet
    '''
    for i in range(0, 4):
        for j in range(0, 6):
            if current_board[j][i] == current_board[j][i+1] == current_board[j][i+2] == current_board[j][i+3] != "_":
                return True, False
    for i in range(0, 7):
        for j in range(0, 3):
            if current_board[j][i] == current_board[j+1][i] == current_board[j+2][i] == current_board[j+3][i] != "_":
                return True, False
    for i in range(0, 4):
        for j in range(0, 3):
            if current_board[j][i] == current_board[j+1][i+1] == current_board[j+2][i+2] == current_board[j+3][i+3] != "_":
                return True, False
    for i in range(0, 4):
        for j in range(5, 2, -1):
            if current_board[j][i] == current_board[j-1][i+1] == current_board[j-2][i+2] == current_board[j-3][i+3] != "_":
                return True, False
    for column in current_board:
        tie = set(column)
        if not tie.__contains__("_"):
            return True, True
        else:
            return False, False

def main_menu_again():
    '''
    This function is called when asking about a player's intention to quit the game
    '''
    response = input("Press 'P' to play again or any other key to quit: ")
    print("")
    return response.strip().lower() == 'p'

class GetResponse():
    '''
    This class exists to receive the responses from either computers or humans, depending on the mode
    '''
    def __init__(self, mode):
        self.mode = mode
    def get_selection(self, counter, current_board, playerNames):
        '''
        This code was modified from my own tictactoe.py script from a previous project.
        This function is called to get the selection of a human user
        '''
        while True:
            try:
                user_selection = int(input("{}, Which column would you like to select: ".format(playerNames[counter].strip())))
                if user_selection in range(1, 8) and current_board[0][user_selection-1] == "_":
                    break
                else:
                    print("Invalid Response")
            except ValueError:
                print("Invalid Response")
        return int(user_selection)
    def generate_selection(self, current_board):
        '''
        This function is called to get the selection of the computer
        '''
        while True:
            generate = randint(1,7)
            if current_board[0][generate-1] == "_":
                break
            else:
                pass
        return generate

class SetBoard():
    '''
    This class exists to modify the board, whether to create a new one or to update an existing one based on user input
    '''
    def new_board (self):
        '''
        This function exists to create a new board
        '''
        board = [["_"], ["_"], ["_"], ["_"], ["_"], ["_"]]
        for row in board:
            for i in range(0, 6):
                row.append("_")
            print(row)
        print("")
        return board
    def update_board(self, current_board, position, mode, counter):
        '''
        This function exists to modify the board based on user input and to print out the board for the user
        '''
        board = SetBoard.change_position(self, current_board, position, mode, counter)
        for row in board:
            print(row)
        return board
    def change_position(self, current_board, position, mode, counter):
        '''
        This function exists to modify the board based on user input, in the background
        '''
        board = current_board
        if counter == 0:
            marker = "X"
        else:
            marker = "O"
        for i in range(5, -1, -1):
            if board[i][position - 1] == "_":
                board[i][position-1] = marker
                break
            else:
                pass
        return board

class PlayGame():
    '''
    This parent class exists to enclose the game played in either solo or PVP mode, to allow for polymorphism
    '''
    def __init__(self, game_over, playerNames, mode, current_board):
        self.game_over = game_over
        self.playerNames = playerNames
        self.mode = mode
        self.current_board = current_board
    def play (self):
        raise NotImplementedError("Subclass must implement abstract method")
    def restart(self):
        raise NotImplementedError("Subclass must implement abstract method")

class PlaySolo(PlayGame):
    '''
    This class exists to be used to play the game against a computer
    '''
    def play(self):
        '''
        This method is called when the game is being played in single player mode and it encompasses all the main logic of the game
        '''
        over = False
        shuffle(playerNames)
        while not over:
            for i in range(0, 1):
                selection = select.get_selection(i, self.current_board, self.playerNames)
                current_board = boardSet.update_board(self.current_board, selection, self.mode, i)
                print("")
                done, tie = check_win(current_board)
                if done:
                    if tie:
                        print("The game has ended in a tie")
                    else:
                        print("The game is over. You have won!")
                    over = True
                    break
                else:
                    pass
                generated = select.generate_selection(current_board)
                current_board = boardSet.update_board(current_board, generated, self.mode, i+1)
                print("")
                done, tie = check_win(current_board)
                if done:
                    if tie:
                        print("The game has ended in a tie")
                    else:
                        print("The game is over. The computer has won!")
                    over = True
                    break
                else:
                    pass
    def restart(self):
        '''
        This method is called when the game is being played in single player mode and it is used to determine if the user wants to restart the mode
        '''
        restart = input("Press 'P' to Play the computer again or any other key to return to the home menu: ")
        return restart.strip().lower() == 'p'

class PlayMultiPlayer(PlayGame):
    '''
    This class exists when the game is being played in PVP mode
    '''
    def play(self):
        '''
        This method is called when the game is being played in PVP mode and it encompasses all the main logic of the game
        '''
        over = False
        shuffle(playerNames)
        while not over:
            for i in range(0, 2):
                selection = select.get_selection(i, self.current_board, self.playerNames)
                current_board = boardSet.update_board(self.current_board, selection, self.mode, i)
                print("")
                done, tie = check_win(current_board)
                if done:
                    if tie:
                        print("The game has ended in a tie")
                    else:
                        print("The game is over. {} has won!".format(playerNames[i]))
                    over = True
                    break
                else:
                    pass
    def restart(self):
        '''
        This method is called when the game is being played in PVP mode and it is used to determine if the user wants to restart the mode
        '''
        restart = input("Press 'P' to Play the computer again or any other key to return to the home menu: ")
        print("")
        return restart.strip().lower() == 'p'

if __name__ == "__main__":
    '''
    This code ensures the game will only run when being run directly from this module
    '''
    main_menu = True
    while main_menu:
        restart = True
        game_over = False
        playerNames, mode = start_game()
        boardSet = SetBoard()
        select = GetResponse(mode)
        current_board = boardSet.new_board()
        while restart:
            if mode == 0:
                game = PlaySolo(game_over, playerNames, mode, current_board)
            else:
                game = PlayMultiPlayer(game_over, playerNames, mode, current_board)
            game.play()
            restart = game.restart()
            if restart:
                game_over = False
                current_board = boardSet.new_board()
            else:
                pass
        main_menu = main_menu_again()
