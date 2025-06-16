from ursina import Entity, Vec3

class Piece(Entity):
    def __init__(self, position=(0, 0, 0), color=None, name="", **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        self.name = name
        self.board_position = (int(position[0]), int(position[2]))  # (x, z)

    def get_legal_moves(self, board):
        return []
