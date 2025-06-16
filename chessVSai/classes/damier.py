from ursina import color, Entity, Vec3
boardmap=[]

class BoardTile(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        boardmap.append(self)
    def on_click(self):
        print(f"Case cliquée à {self.name},at,{self.position}")

class Board:
    TAILLE = 8

    def __init__(self):
        self.tiles = []
        self.state = [[None for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]
        self.pieces = []  # store all active pieces (for AI too)

        for x in range(self.TAILLE):
            for z in range(self.TAILLE):
                color_case = color.white if (x + z) % 2 == 0 else color.black
                letter = chr(ord('A') + x)
                number = str(z + 1)
                tile_name = f'{letter}-{number}'
                tile = BoardTile(position=(x, -1, z), color=color_case, name=tile_name)
                self.tiles.append(tile)

    def add_piece(self, piece, x, z):
        self.state[x][z] = piece
        self.pieces.append(piece)
        piece.board_position = (x, z)

    def move_piece(self, piece, to_x, to_z):
        from_x, from_z = piece.board_position
        self.state[from_x][from_z] = None
        captured = self.state[to_x][to_z]
        self.state[to_x][to_z] = piece
        piece.board_position = (to_x, to_z)
        piece.position = Vec3(to_x, 0, to_z)
        if captured:
            self.pieces.remove(captured)
        return captured  # So we can undo it

    def undo_move(self, piece, from_pos, to_pos, captured_piece):
        fx, fz = from_pos
        tx, tz = to_pos
        self.state[tx][tz] = captured_piece
        self.state[fx][fz] = piece
        piece.board_position = from_pos
        piece.position = Vec3(fx, 0, fz)
        if captured_piece:
            self.pieces.append(captured_piece)


