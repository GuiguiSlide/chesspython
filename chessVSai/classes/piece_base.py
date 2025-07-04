from ursina import Entity, Vec3

class Piece(Entity):
    def __init__(self, position=(0, 0, 0), color=None, name="", **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            collider='box',
            **kwargs
        )
        self.name = name
        self.board_position = (int(position[0]), int(position[2]))  # (x, z)

    def get_legal_moves(self, board):
        return []
