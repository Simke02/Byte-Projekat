class Move:
    def __init__(self, row, column, stackPosition, direction) -> None:
        self.row = row
        self.column = column
        self.stackPosition = stackPosition
        self.direction = direction