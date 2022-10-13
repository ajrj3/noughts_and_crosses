import numpy as np
import tkinter as tk
from tkinter import font as tkFont
from functools import partial


class Game():
    def __init__(self):
        self.winner = None
        self.game_over = False
        self.player = 'O'
        self.game_states = [[],[],[]]  # save game history (for undo function)
        self.turn_counter = 0

        self.root = tk.Tk()
        helv18 = tkFont.Font(family='Helvetica', size=18, weight=tkFont.BOLD)
        helv24 = tkFont.Font(family='Helvetica', size=24, weight=tkFont.BOLD)

        self.root.wm_attributes('-toolwindow', 'True')  # remove tkinter feather icon
        self.root.title('Noughts and crosses')
        self.root.configure(background='white')

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.game_grid = np.zeros((3,3))    # used for checking game status (see if there is a winner)
        self.GUI_grid = np.empty(shape=(3,3), dtype='object')   # array that stores Tkinter Button objects

        for i, row in enumerate(self.GUI_grid):
            for j, _ in enumerate(row):
                func = partial(self.turn,i,j)   # https://www.learnpython.org/en/Partial_functions
                self.GUI_grid[i,j] = tk.Button(self.main_frame, text=' ', font=helv24, bg='white', fg='black', height=4, width=8)
                self.GUI_grid[i,j].grid(row=i, column=j)       
                self.GUI_grid[i,j].configure(command=func)

        self.button_frame = tk.Frame(self.root, bg='white')
        self.button_frame.pack(side='bottom', pady=10)
        self.reset_button = tk.Button(self.button_frame, text='Reset', font=helv18, bg='white', fg='black', command=self.reset_game)
        self.undo_button = tk.Button(self.button_frame, text='Undo', font=helv18, bg='white', fg='black', command=self.undo)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.reset_button.grid(row=0, column=0, sticky=tk.W+tk.E, padx=15)
        self.undo_button.grid(row=0, column=1, sticky=tk.W+tk.E, padx=15)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side='top', pady=25)
        self.output_text = tk.Label(self.output_frame, text=f'{self.player}\'s turn', font=helv18, bg='white', fg='black')
        self.output_text.pack()

        self.game_states[0].append([entry['text'] for entry in np.ravel(self.GUI_grid)])
        self.game_states[1].append(np.copy(self.game_grid))
        self.game_states[2].append(f'{self.player}\'s turn')

        self.root.mainloop()

    def update_game(self, x, y):
        if self.GUI_grid[x, y]['text'] == ' ':
            if self.player == 'X':
                self.GUI_grid[x, y]['text'] = 'X'
                self.game_grid[x, y] = 1
                self.game_states[2].append(f'O\'s turn')
                self.player = 'O'
            else:
                self.GUI_grid[x, y]['text'] = 'O'
                self.game_grid[x, y] = -1
                self.game_states[2].append(f'X\'s turn')
                self.player = 'X'
            self.turn_counter += 1
            self.game_states[0].append([entry['text'] for entry in np.ravel(self.GUI_grid)])
            self.game_states[1].append(np.copy(self.game_grid))
                
        return self
    
    def check_winner(self):
        test_submatrix1 = np.array([sum(self.game_grid[:,i] for i in range(3))])    # check if there is a winning column
        test_submatrix2 = np.array([sum(self.game_grid[i,:] for i in range(3))])    # check rows
        test_submatrix3 = np.array([sum(self.game_grid[i,i] for i in range(3))])    # check one diagonal
        test_submatrix4 = np.array([sum(self.game_grid[2-i,i] for i in range(3))])  # check other diagonal
        test_matrix = np.column_stack((test_submatrix1, test_submatrix2, test_submatrix3, test_submatrix4))

        for marker, player in zip([1,-1], ['X', 'O']):
            test_condition = np.where(test_matrix == 3*marker, True, False).any()
            if test_condition:
                self.game_over = True
                self.winner = player
                break
        if np.all(self.game_grid) and self.winner == None:
            self.game_over = True

        return self

    def turn(self,i,j):
        if self.game_over == False:
            self.update_game(i,j)
            self.check_winner()
            self.output_text.configure(text=f'{self.player}\'s turn')

        if self.game_over == True and self.winner is not None:
            self.output_text.configure(text=f'{self.winner}\'s has won!')
        elif self.game_over == True:
            self.output_text.configure(text=f'Draw!')

        return self

    def reset_game(self):
        self.winner = None
        self.game_over = False
        self.player = 'O'
        self.game_states = [[],[],[]]
        self.turn_counter = 0
        self.game_grid = np.zeros((3,3))
        for entry in np.ravel(self.GUI_grid):
            entry.configure(text=' ')

        self.game_states[0].append([entry['text'] for entry in np.ravel(self.GUI_grid)])
        self.game_states[1].append(np.copy(self.game_grid))
        self.game_states[2].append(f'{self.player}\'s turn')

        return self
    
    def undo(self):
        if self.turn_counter == 0:
            return self
        else:
            self.turn_counter -= 1
            for entry, prev_state in zip(np.ravel(self.GUI_grid), self.game_states[0][self.turn_counter]):
                entry.configure(text = prev_state)
            self.output_text.configure(text=self.game_states[2][self.turn_counter])
            del self.game_states[0][-1]
            del self.game_states[1][-1]
            del self.game_states[2][-1]
            
            return self

    
game = Game()