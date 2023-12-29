from Move import Move
import math

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
        self.win = False
        self.figures_count = 0
        self.turn = 0
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

    def enter_move(self, figure):
        wholeMove = input("Enter move: ")
        move_list = wholeMove.split()
        if(len(move_list) != 4):
            return False

        rowNum = abs(ord('A') - ord(move_list[0]))
        column = int(move_list[1]) - 1
        stack_position = int(move_list[2])

        if(self.isMoveValid(rowNum, column, stack_position, move_list[3], figure)):
            next_location = self.MoveToLocation(Move(rowNum, column, stack_position, move_list[3]))
            count = self.numberOfElementInStack((rowNum, column))
                                    
            num_of_elements = count - stack_position
            position = self.matrix[next_location[0]][next_location[1]].index('.')
            for i in range(num_of_elements):
                self.matrix[next_location[0]][next_location[1]][position+i] = self.matrix[rowNum][column][stack_position+i]
                self.matrix[rowNum][column][stack_position+i]='.'

            count_next = self.numberOfElementInStack(next_location)
            if(count_next > 7):
                if (self.matrix[next_location[0]][next_location[1]][8]=='X'):
                    self.Xscore+=1
                else:
                    self.Oscore+=1  
                for i in range(9):
                    self.matrix[next_location[0]][next_location[1]][i]='.' 
                self.figures_count-=8 
            self.turn += 1
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
    def figureExistsInStackPosition(self, row, column, stack_position, figure):
        
        if(0 <= stack_position < 9):
            if(self.matrix[row][column][stack_position] == figure):
                return True
        return False
    
    def moveInMoves(self, move):
        if(move in self.moves):
            return True
        return False
    
    def finished_game(self):
        if(self.figures_count == 0 or
            self.Xscore > 0 or
              self.Oscore > 0):
            return True
        return False
    
    def surroundingFieldsAreEmpty(self, move):
        empty = True
        if(move.row > 0):
            if(move.column > 0):
                if(self.matrix[move.row - 1][move.column - 1][0] != '.'):
                    empty = False
            if(move.column < 7):
                if(self.matrix[move.row - 1][move.column + 1][0] != '.'):
                    empty = False
        if(move.row < 7):
            if(move.column > 0):
                if(self.matrix[move.row + 1][move.column - 1][0] != '.'):
                    empty = False
            if(move.column < 7):
                if(self.matrix[move.row + 1][move.column + 1][0] != '.'):
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
                #Gore levo
                if(self.existsInTable(node[0] - 1, node[1] - 1)):
                    if((node[0] - 1, node[1] - 1) not in visited):
                        if(self.figureExistsInField(node[0] - 1, node[1] - 1)):
                            notFound = False, locations.add((node[0] - 1, node[1] - 1))
                        visited.add((node[0] - 1, node[1] - 1))
                        needToStartFrom2.add((node[0] - 1, node[1] - 1))

                #Gore desno
                if(self.existsInTable(node[0] - 1, node[1] + 1)):
                    if((node[0] - 1, node[1] + 1) not in visited):
                        if(self.figureExistsInField(node[0] - 1, node[1] + 1)):
                            notFound = False, locations.add((node[0] - 1, node[1] + 1))
                        visited.add((node[0] - 1, node[1] + 1))
                        needToStartFrom2.add((node[0] - 1, node[1] + 1))
            
                #Dole levo
                if(self.existsInTable(node[0] + 1, node[1] - 1)):
                    if((node[0] + 1, node[1] - 1) not in visited):
                        if(self.figureExistsInField(node[0] + 1, node[1] - 1)):
                            notFound = False, locations.add((node[0] + 1, node[1] - 1))
                        visited.add((node[0] + 1, node[1] - 1))
                        needToStartFrom2.add((node[0] + 1, node[1] - 1))

                #Dole desno
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
        emptySurroundingFields = self.surroundingFieldsAreEmpty(move)
        if(move.stackPosition < numOfElements or emptySurroundingFields):
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

        if(self.Xscore > self.Oscore):
            winner_found = "X"
            
        elif(self.Oscore > self.Xscore):
            winner_found = "O"
        else:
            winner_found = "Draw" 
        
        return winner_found
            
    def allPossibleMoves(self, active_player):
        allMoves = set()
        for i in range(self.size):
            for j in range(self.size):
                z = 0
                while(self.matrix[i][j][z]!=" " and self.matrix[i][j][z]!="."):
                    if(self.matrix[i][j][z]==active_player):
                        newMoves = self.validMovesForConcreteFigure(i, j, z, active_player)
                        if(newMoves != None):
                            allMoves.update(newMoves)
                    z+=1
        return allMoves

    def isMoveValid(self, rowNum, column, stack_position, direction, figure):

        if(self.existsInTable(rowNum, column)):
            if(self.figureExistsInField(rowNum, column)):
                if(self.figureExistsInStackPosition(rowNum, column, stack_position, figure)):
                    if(self.moveInMoves(direction)):
                        next_location = self.MoveToLocation(Move(rowNum, column, stack_position, direction))
                        if(next_location != False):
                            if(self.isItLeadingToNearestStack(Move(rowNum, column, stack_position, direction))):
                                if(self.canMoveStackOnStack(Move(rowNum, column, stack_position, direction))):
                                    return True
        return False
    
    def validMovesForConcreteFigure(self, rowNum, column, stack_position, active_player):
        validMoves = set()
        for direction in self.moves:
            if(self.isMoveValid(rowNum, column, stack_position, direction, active_player)):
                validMoves.add(Move(rowNum, column, stack_position, direction))
        if(len(validMoves) == 0):
            return None
        return validMoves
    
    def printingAllPossibleMoves(self, active_player):
        Move.printMovesForPlayer(self.allPossibleMoves(active_player))

    def playAllMoves(self, allMoves):
        allTables = set()
        for move in allMoves:
            table = Table(self.size)
            table.copyTable(self)
            table.playMove(move)
            allTables.add(table)
        return allTables

    def getNextMove(self, depth, player):
        value = self.alphaBeta(depth, -math.inf, math.inf, player)
        move = self.findTheDifference(value[1])
        return move

    def alphaBeta(self, depth, alpha, beta, player):
        allMoves = self.allPossibleMoves(player)
        allTables = self.playAllMoves(allMoves)
        if depth == 0 or len(allMoves) == 0:
            #Treba da se vrati vrednost heuristike i cela tabela
            return self.heuristicValue(depth, player)
        # X je maksimajzing plejer
        if player == 'X':
            #Zapamti da value treba da sadrzi i info o potezu ili tabeli
            value = (-math.inf, self)
            for table in allTables:
                new_value = table.alphaBeta(depth-1, alpha, beta, 'O')
                if new_value[0] > value[0]:
                    value = new_value
                #value = max(value, table.alphaBeta(depth-1, alpha, beta, 'O'))
                if value[0] > beta:
                    break
                alpha = max(alpha, value[0])
            return value
        else:
            value = (math.inf, self)
            for table in allTables:
                new_value = table.alphaBeta(depth-1, alpha, beta, 'X')
                if new_value[0] < value[0]:
                    value = new_value
                #value = min(value, table.alphaBeta(depth-1, alpha, beta, 'X'))
                if value[0] < alpha:
                    break
                beta = min(beta, value[0])
            return value
        
    def copyTable(self, table):
        self.player1 = table.player1
        self.figure1 = table.figure1
        self.player2 = table.player2
        self.figure2 = table.figure2
        self.Xscore = table.Xscore
        self.Oscore = table.Oscore
        self.maxStack = table.maxStack
        self.win = table.win
        self.figures_count = table.figures_count
        for i in range(self.size):
            for j in range(self.size):
                for z in range(9):
                    self.matrix[i][j][z] = table.matrix[i][j][z]
        
    def playMove(self, move):
        count_of_figures = self.numberOfElementInStack((move.row, move.column))
        figures_to_move = count_of_figures - move.stackPosition
        top_of_stack = 0
        i = 0
        location = self.MoveToLocation(move)
        while i < 9 or self.matrix[location[0]][location[1]][i] != '.':
            top_of_stack += 1
            i += 1
        for i in range(figures_to_move):
            self.matrix[location[0]][location[1]][top_of_stack + i] = self.matrix[move.row][move.column][move.stackPosition + i]
            self.matrix[move.row][move.column][move.stackPosition + i] = '.'
        self.turn += 1
        new_number_of_figures = self.numberOfElementInStack(location)
        if(new_number_of_figures > 7):
            if (self.matrix[location[0]][location[1]][8]=='X'):
                self.Xscore+=1
            else:
                self.Oscore+=1  
            for i in range(9):
                self.matrix[location[0]][location[1]][i]='.' 
            self.figures_count-=8 
        self.turn += 1

    def heuristicValue(self, depth, player):
        if depth != 0:
            if self.finished_game():
                if self.declare_winner == 'X':
                    return (1, self)
                elif self.declare_winner == 'O':
                    return (-1, self)
                else:
                    return (0, self)
        else:
            location = self.findBiggestStack()
            distance = self.shortestFigureToBiggestStack(location)
            moves_counter = 16 - depth
            probability = (moves_counter/distance)/100
            if player == 'O':
                probability = -1*probability
            return (probability, self)
    
    def findBiggestStack(self):
        locationR = ()
        countR = 0
        countL = 0
        for i in range(self.size):
            for j in range(self.size):
                countL = self.numberOfElementInStack((i, j))
                if countR < countL:
                    locationR = (i, j)
        return locationR
    
    def shortestFigureToBiggestStack(self, location):
        return
    
    def findTheDifference(self, table):
        locationSelf = ()
        locationTable = ()
        for i in range(self.size):
            for j in range(self.size):
                for z in range(9):
                    if self.matrix[i][j][z] != table.matrix[i][j][z]:
                        if self.matrix[i][j][z] == '.':
                            locationSelf = (i, j, z)
                            break

        if(self.existsInTable(locationSelf[0] - 1, locationSelf[1] - 1)):
            for i in range(9):
                if self.matrix[locationSelf[0] - 1][locationSelf[1] - 1][i] != table.matrix[locationSelf[0] - 1][locationSelf[1] - 1][i]:
                    return Move(locationSelf[0], locationSelf[1], locationSelf[2], 'GL')

        if(self.existsInTable(locationSelf[0] - 1, locationSelf[1] + 1)):
            for i in range(9):
                if self.matrix[locationSelf[0] - 1][locationSelf[1] + 1][i] != table.matrix[locationSelf[0] - 1][locationSelf[1] + 1][i]:
                    return Move(locationSelf[0], locationSelf[1], locationSelf[2], 'GD')
                    
        if(self.existsInTable(locationSelf[0] + 1, locationSelf[1] - 1)):
            for i in range(9):
                if self.matrix[locationSelf[0] + 1][locationSelf[1] - 1][i] != table.matrix[locationSelf[0] + 1][locationSelf[1] - 1][i]:
                    return Move(locationSelf[0], locationSelf[1], locationSelf[2], 'DL')

        if(self.existsInTable(locationSelf[0] + 1, locationSelf[1] + 1)):
            for i in range(9):
                if self.matrix[locationSelf[0] + 1][locationSelf[1] + 1][i] != table.matrix[locationSelf[0] + 1][locationSelf[1] + 1][i]:
                    return Move(locationSelf[0], locationSelf[1], locationSelf[2], 'DD')
        