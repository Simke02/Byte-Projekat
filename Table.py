from Move import Move

class Table:
    def __init__(self, size) -> None:
        self.size = size
        self.moves = ["GL", "GD", "DL", "DD"]
        self.player1 = "H"
        self.figure1 = "X"
        self.player2 = "C"
        self.figure2 = "O"
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
                #if(i > 1 and i < self.size - 1):
                    self.matrix[i][j][0] = figure 
                j += 2
        self.figures_count = (self.size - 2) * (self.size / 2)
        self.maxStack = self.figures_count / 8

        #self.matrix[0][2][0] = figure 
    
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

        rowNum = abs(ord('A') - ord(move_list[0]))
        column = int(move_list[1]) - 1
        if(self.existsInTable(rowNum, column)):
            if(self.figureExistsInField(rowNum, column)):
                if(self.figureExistsInStackPosition(rowNum, column, int(move_list[2]))):
                    if(self.moveInMoves(move_list[3])):
                        if(self.MoveToLocation(Move(rowNum, column, int(move_list[2]), move_list[3])) != False):
                            return True
        return False

    def existsInTable(self, row, column):
        if(0 <= row < self.size):
            if(0 <= column < self.size):
                return True
        return False
    
    def figureExistsInField(self, row, column):
        if('X' in self.matrix[row][column] or
            'O' in self.matrix[row][column]):
            return True
        return False
    
    #Proveri da li je igrac igra sa svojom figurom
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
    
    def surroundingFieldsAreEmpty(self, move):
        empty = True
        if(move.row > 0):
            if(move.column > 0):
                if(len(self.matrix[move.row - 1][move.column - 1]) != 0):
                    empty = False
            if(move.column < 7):
                if(len(self.matrix[move.row - 1][move.column + 1]) != 0):
                    empty = False
        if(move.row < 7):
            if(move.column > 0):
                if(len(self.matrix[move.row + 1][move.column - 1]) != 0):
                    empty = False
            if(move.column < 7):
                if(len(self.matrix[move.row + 1][move.column + 1]) != 0):
                    empty = False
        return empty
    
    def isItLeadingToNearestStack(self, move):
        locations = set()
        notFound = True
        iterator = 0
        needToStartFrom1 = {(move.row, move.column)}
        needToStartFrom2 = set()
        visited = {(move.row, move.column)}
        while(notFound == True):
            if(iterator != 0):
                needToStartFrom1.clear()
                needToStartFrom1.update(needToStartFrom2)
                needToStartFrom2.clear()
                iterator += 1
            else:
                iterator += 1

            for node in needToStartFrom1:
                if(self.existsInTable(node[0] - 1, node[1] - 1)):
                    if((node[0] - 1, node[1] - 1) not in visited):
                        if(self.figureExistsInField(node[0] - 1, node[1] - 1)):
                            notFound = False, locations.add((node[0] - 1, node[1] - 1))
                        visited.add((node[0] - 1, node[1] - 1))
                        needToStartFrom2.add((node[0] - 1, node[1] - 1))

                if(self.existsInTable(node[0] - 1, node[1] + 1)):
                    if((node[0] - 1, node[1] + 1) not in visited):
                        if(self.figureExistsInField(node[0] - 1, node[1] + 1)):
                            notFound = False, locations.add((node[0] - 1, node[1] + 1))
                        visited.add((node[0] - 1, node[1] + 1))
                        needToStartFrom2.add((node[0] - 1, node[1] + 1))
            
                if(self.existsInTable(node[0] + 1, node[1] - 1)):
                    if((node[0] + 1, node[1] - 1) not in visited):
                        if(self.figureExistsInField(node[0] + 1, node[1] - 1)):
                            notFound = False, locations.add((node[0] + 1, node[1] - 1))
                        visited.add((node[0] + 1, node[1] - 1))
                        needToStartFrom2.add((node[0] + 1, node[1] - 1))
            
                if(self.existsInTable(node[0] + 1, node[1] + 1)):
                    if((node[0] + 1, node[1] + 1) not in visited):
                        if(self.figureExistsInField(node[0] + 1, node[1] + 1)):
                            notFound = False, locations.add((node[0] + 1, node[1] + 1))
                        visited.add((node[0] + 1, node[1] + 1))
                        needToStartFrom2.add((node[0] + 1, node[1] + 1))
        
        location = self.MoveToLocation(move)
        if(location == False):
            return False
        if(location in locations):
            return True
        
        notFound = True
        iterator2 = 0
        needToStartFrom1 = {location}
        needToStartFrom2 = set()
        visited = {location, (move.row, move.column)}
        while(notFound == True and iterator2 < iterator):
            if(iterator2 != 0):
                needToStartFrom1.clear()
                needToStartFrom1.update(needToStartFrom2)
                needToStartFrom2.clear()
                iterator2 += 1
                if(iterator2 == iterator):
                    continue
            else:
                iterator2 += 1

            for node in needToStartFrom1:
                if(self.existsInTable(node[0] - 1, node[1] - 1)):
                    if((node[0] - 1, node[1] - 1) not in visited):
                        if((node[0] - 1, node[1] - 1) in locations):
                            notFound = False
                            break
                        visited.add((node[0] - 1, node[1] - 1))
                        needToStartFrom2.add((node[0] - 1, node[1] - 1))

                if(self.existsInTable(node[0] - 1, node[1] + 1)):
                    if((node[0] - 1, node[1] + 1) not in visited):
                        if((node[0] - 1, node[1] + 1) in locations):
                            notFound = False
                            break
                        visited.add((node[0] - 1, node[1] + 1))
                        needToStartFrom2.add((node[0] - 1, node[1] + 1))
            
                if(self.existsInTable(node[0] + 1, node[1] - 1)):
                    if((node[0] + 1, node[1] - 1) not in visited):
                        if((node[0] + 1, node[1] - 1) in locations):
                            notFound = False
                            break
                        visited.add((node[0] + 1, node[1] - 1))
                        needToStartFrom2.add((node[0] + 1, node[1] - 1))
            
                if(self.existsInTable(node[0] + 1, node[1] + 1)):
                    if((node[0] + 1, node[1] + 1) not in visited):
                        if((node[0] + 1, node[1] + 1) in locations):
                            notFound = False
                            break
                        visited.add((node[0] + 1, node[1] + 1))
                        needToStartFrom2.add((node[0] + 1, node[1] + 1))

        if(notFound == False and iterator2 < iterator):
            return True
        
    
    def MoveToLocation(self, move):
        if(move.direction == self.moves[0]):
            if(self.existsInTable(move.row - 1, move.column - 1)):
                return (move.row - 1, move.column - 1)
            else:
                return False
            
        if(move.direction == self.moves[1]):
            if(self.existsInTable(move.row - 1, move.column + 1)):
                return (move.row - 1, move.column + 1)
            else:
                return False
            
        if(move.direction == self.moves[2]):
            if(self.existsInTable(move.row + 1, move.column - 1)):
                return (move.row + 1, move.column - 1)
            else:
                return False
    
        if(move.direction == self.moves[3]):
            if(self.existsInTable(move.row + 1, move.column + 1)):
                return (move.row + 1, move.column + 1)
            else:
                return False
            
    def canMoveStackOnStack(self, move):
        location = self.MoveToLocation(move)
        if(location == False):
            return False
        numOfElements = self.numberOfElementInStack(location)
        currentStackNumOfElements = self.numberOfElementInStack((move.row, move.column))
        if(move.stackPosition < numOfElements):
            if(currentStackNumOfElements - move.stackPosition + numOfElements < 9):
                return True
        return False


    def numberOfElementInStack(self, location):
        count = 0
        for element in self.matrix[location[0]][location[1]]:
            if(element == 'X' or element == 'O'):
                count += 1
        return count
    
    def declare_winner(self):
        
        
        #ovde se ispita ko je pobednik
        ##winner_found = self.finished_game()
        if(self.Xscore < self.Oscore):
            winner_found = "X"
            
        elif(self.Oscore < self.Xscore):
            winner_found = "O"
        else:
            winner_found = "Draw" 
        
        return winner_found
            