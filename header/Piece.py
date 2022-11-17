from header.data_game import SPRITES, TETROMINOS, tetrominos_colors


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = tetrominos_colors[TETROMINOS.index(shape)]
        self.rotation = 0  # number from 0-3
        self.pixel = SPRITES[TETROMINOS.index(shape)]
