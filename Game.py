from Table import Table
from Move import Move

class Game:
    def __init__(self) -> None:
        self.size = 0
        self.active_player = True

    def set_table(self):
        correct_value = True 
        while(correct_value):
            user_input = input("Enter the size of table: ")
            try:
                self.size = int(user_input)
            except:
                print("Invalid value entered")
                continue
            if(self.size < 17 and self.size % 2 == 0 and (((self.size - 2) * (self.size / 2)) % 8) == 0):
                self.table = Table(self.size)
                correct_value = False
            else:
                print("Invalid value entered")
        self.table.init_table()

        correct_value = True 
        while(correct_value):
            user_input = input("Enter the first player (H/C), his figure (X/O) and enter second player (H/C): ")
            players = user_input.split()
            if(len(players) == 3):
                if(players[0] == 'H' or players[0] == 'C'):
                    if(players[1] == 'X' or players[1] == 'O'):
                        if(players[2] == 'H' or players[2] == "C"):
                            self.table.player1 = players[0]
                            self.table.figure1 = players[1]
                            self.table.player2 = players[2]
                            self.table.figure2 = 'O' if players[1]=='X' else 'X'
                            correct_value = False
                            continue
            print("Invalid value entered")

    def draw_table(self):
        self.table.draw_table()

    def declare_winner(self):
        winner = self.table.declare_winner()
        if(winner == "Draw"):
            print("Draw")
        print("winner is " + winner)
    
    def enter_move(self, figure):
        canMove = False
        
        while(not canMove):
            canMove = self.table.enter_move(figure)

        game.draw_table()
        self.active_player = not self.active_player
       

    def play(self):
        while(not self.table.win):
            if(self.active_player):
                fig = game.table.figure1
            else:
                fig = game.table.figure2
            print('Player ' + fig, end=" ")
            self.enter_move(fig)
             
            if(self.table.finished_game()):
                self.declare_winner()
                self.table.win= True   
            


game = Game()
game.set_table()
game.draw_table()
game.play()
