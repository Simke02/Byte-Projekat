class Table:
    def __init__(self, size) -> None:
        self.size = size
        self.moves = {"GL", "GD", "DL", "DD"}
        self.player = "H"
        self.figure = "X"
        self.Xscore = 0
        self.Oscore = 0
        self.maxStack = 0
        self.figures_count = 0
        self.matrix = [[[" " for _ in range(9)] for _ in range(self.size)]
                       for _ in range(self.size)]
        
    def init_table(self):
        for i in range(self.size):
            beginValue = 0
            figure = 'O'
            if(i % 2 != 0):
                beginValue = 1
                figure = 'X'
            j = beginValue
            while j < self.size:
                for z in range(9):
                    self.matrix[i][j][z] = "."
                if(i > 0 and i < self.size - 1):
                    self.matrix[i][j][0] = figure 
                j += 2
        self.figures_count = (self.size - 2) * (self.size / 2)
        self.maxStack = self.figures_count / 8
    
    def draw_table(self):
        print("  ", end=" ")
        brojac = 1
        for i in range(self.size):
            for j in range(3):
                if(j == 1):
                    print(brojac, end=" ")
                elif(j == 0 and i >= 10):
                    print("", end=" ")
                else:
                    print(" ", end=" ")
            brojac += 1
            if(i < 10): 
                print(" ", end=" ")
            else:
                print(" ", end=" ")

        print()

        slovo = 'A'
        for i in range(self.size):
            for y in range(3):
                if(y==1):
                    print(slovo + " ", end=" ")
                    slovo = chr(ord(slovo) + 1)
                else:
                    print("  ", end=" ")
                for j in range(self.size):
                    for z in range(2, -1, -1):
                        print(self.matrix[i][j][8 - (z + y * 3)], end=' ')
                        if(z == 0):
                            print(" ", end=' ')
                    if(j == self.size - 1):
                        print()
                if(y == 2):
                    print()
        print("X: " + str(self.Xscore) + "  O: " + str(self.Oscore))

    def enter_move(self):
        wholeMove = input("Enter move: ")
        move_list = wholeMove.split()
        if(len(move_list) != 4):
            return False

        if(self.existsInTable(move_list[0], int(move_list[1]))):
            rowNum = abs(ord('A') - ord(move_list[0]))
            column = int(move_list[1]) - 1
            if(self.figureExistsInField(rowNum, column)):
                if(self.figureExistsInStackPosition(rowNum, column, int(move_list[2]))):
                    if(self.moveInMoves(move_list[3])):
                        return True
        return False

    def existsInTable(self, row, column):
        if(type(row) is str):
            if('A' <= row <= chr(ord('A') + self.size - 1)):
                if(type(column) is int):
                    if(0 < column <= self.size):
                        return True
        return False
    
    def figureExistsInField(self, row, column):
        if('X' in self.matrix[row][column] or
            'O' in self.matrix[row][column]):
            return True
        return False
    
    #Proveri da li je pravi igrac
    def figureExistsInStackPosition(self, row, column, stack_position):
        if(0 <= stack_position < 9):
            if(self.matrix[row][column][stack_position] == 'X'
                or self.matrix[row][column][stack_position] == 'O'):
                return True
        return False
    
    def moveInMoves(self, move):
        if(move in self.moves):
            return True
        return False
    
    def finished_game(self):
        if(self.figures_count == 0 or
            self.Xscore > self.maxStack/2 or
              self.Oscore > self.maxStack/2):
            return True
        return False