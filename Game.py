from Table import Table

class Game:
    def __init__(self) -> None:
        self.size = 0

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
            user_input = input("Enter the first player (H/C) and his figure (X/O) ")
            players = user_input.split()
            if(len(players) == 2):
                if(players[0] == 'H' or players[0] == 'C'):
                    if(players[1] == 'X' or players[1] == 'O'):
                        self.table.player = players[0]
                        self.table.figure = players[1]
                        correct_value = False
                        print(self.table.player + self.table.figure)
            print("Invalid value entered")

    def draw_table(self):
        self.table.draw_table()
    
    def enter_move(self):
        return self.table.enter_move()

game = Game()
game.set_table()
game.draw_table()
print(game.enter_move())