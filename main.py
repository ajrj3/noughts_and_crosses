import numpy as np

class GameGrid():
    def __init__(self):
        self.grid = np.zeros((3,3))
        return None
    
    def print_grid(self):
        print(self.grid)
        return None

    def update_grid(self, player, x, y):
        assert x in range(3) and y in range(3), 'Co-ordinate given not in allowable range of 0 to 2'
        if player == 'noughts':
            self.grid[x,y] = 1
        else:
            self.grid[x,y] = -1
        self.print_grid()
        return self


class Game():
    def __init__(self):
        self.game_over = False
        self.winner = None
        self.game_grid = GameGrid()
        self.player = 'noughts'
        return None

    def check_winner(self):
        test_submatrix1 = np.array([np.sum(self.game_grid.grid[:,i] for i in range(3))])
        test_submatrix2 = np.array([np.sum(self.game_grid.grid[i,:] for i in range(3))])
        test_submatrix3 = np.array([np.sum(self.game_grid.grid[i,i] for i in range(3))])
        test_submatrix4 = np.array([np.sum(self.game_grid.grid[2-i,i] for i in range(3))])
        test_matrix = np.column_stack((test_submatrix1, test_submatrix2, test_submatrix3, test_submatrix4))

        for marker, player in zip([1,-1], ['noughts', 'crosses']):
            test_condition = np.where(test_matrix == 3*marker, True, False).any()
            if test_condition:
                self.game_over = True
                self.winner = player
                print(f'{self.winner} is the winner!')
        if np.all(self.game_grid.grid) and self.winner == None:
            self.game_over = True
            print('Draw!')
            
        return self

    def turn(self, player):
        _valid_turn = False
        while _valid_turn is False:
            print(f'{player} turn')
            print("Input desired x co-ord:")
            x_co_ord  = int(input())
            print("Input desired y co-ord:")
            y_co_ord = int(input())
            
            # check validity
            if x_co_ord in range(3) and y_co_ord in range(3) and self.game_grid.grid[x_co_ord, y_co_ord] == 0:
                _valid_turn = True
            else:
                print("Invalid entry, please try again")

        self.game_grid.update_grid(player, x_co_ord, y_co_ord)
        self.check_winner()
        if player == 'noughts':
            self.player = 'crosses'
        else:
            self.player = 'noughts'


# initialise game
game = Game()

# play game
while game.game_over == False:
    game.turn(game.player)