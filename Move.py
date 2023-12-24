class Move:
    def __init__(self, row, column, stackPosition, direction) -> None:
        self.row = row
        self.column = column
        self.stackPosition = stackPosition
        self.direction = direction

    @staticmethod
    def printMovesForPlayer(moves):
        if(len(moves) != 0):
            for move in moves:
                print(chr(65+move.row) + " " + str(move.column + 1) + " " + str(move.stackPosition) + " " + str(move.direction))