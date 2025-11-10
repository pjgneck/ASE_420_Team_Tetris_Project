WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
ORANGE = (255, 125, 0)
YELLOW = (255, 215, 0)
PURPLE = (120, 37, 179)
TEAL = (100, 179, 179)
BROWN = (80, 34, 22)
GREEN = (80, 134, 22)
RED = (180, 34, 22)
MAGENTA = (180, 34, 122)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BLOCK_SIZE = 20

BRIGHT_PURPLE = (200, 100, 255)
BRIGHT_TEAL = (100, 255, 255)
BRIGHT_BROWN = (200, 100, 50)
BRIGHT_GREEN = (100, 255, 100)
BRIGHT_RED = (255, 100, 100)
BRIGHT_MAGENTA = (255, 100, 200)

LIGHT_THEME = {
    "background": WHITE,
    "text": BLACK,
    "grid": GRAY,
    "highlight": YELLOW,
    "game_over": ORANGE
}

DARK_THEME = {
    "background": DARK_GRAY,
    "text": WHITE,
    "grid": LIGHT_GRAY,
    "highlight": YELLOW,
    "game_over": ORANGE
}

PURPLE_BLOCK = 1
TEAL_BLOCK = 2
BROWN_BLOCK = 3
GREEN_BLOCK = 4
RED_BLOCK = 5
MAGENTA_BLOCK = 6

LIGHT_BLOCK_COLORS = {
    PURPLE_BLOCK: PURPLE,
    TEAL_BLOCK: TEAL,
    BROWN_BLOCK: BROWN,
    GREEN_BLOCK: GREEN,
    RED_BLOCK: RED,
    MAGENTA_BLOCK: MAGENTA
}
BLOCK_COLORS = LIGHT_BLOCK_COLORS

DARK_BLOCK_COLORS = {
    PURPLE_BLOCK: BRIGHT_PURPLE,
    TEAL_BLOCK: BRIGHT_TEAL,
    BROWN_BLOCK: BRIGHT_BROWN,
    GREEN_BLOCK: BRIGHT_GREEN,
    RED_BLOCK: BRIGHT_RED,
    MAGENTA_BLOCK: BRIGHT_MAGENTA
}

LIGHT_BLOCK_OUTLINE = BLACK
DARK_BLOCK_OUTLINE = WHITE

SHAPES = [
    # I-shape
    [
        [1, 5, 9, 13],
        # . X . .
        # . X . .
        # . X . .
        # . X . .
        
        [4, 5, 6, 7]
        # . . . .
        # X X X X
        # . . . .
        # . . . .
    ],

    # Z-shape
    [
        [4, 5, 9, 10],
        # . . . .
        # X X . .
        # . X X .
        # . . . .

        [2, 6, 5, 9]
        # . . X .
        # . X X .
        # . X . .
        # . . . .
    ],

    # S-shape
    [
        [6, 7, 9, 10],
        # . . . .
        # . . X X
        # . X X .
        # . . . .

        [1, 5, 6, 10]
        # . X . .
        # . X X .
        # . . X .
        # . . . .
    ],

    # L-shape
    [
        [1, 2, 5, 9],
        # . X X .
        # . X . .
        # . X . .
        # . . . .

        [0, 4, 5, 6],
        # X . . .
        # X X X .
        # . . . .
        # . . . .

        [1, 5, 9, 8],
        # . X . .
        # . X . .
        # X X . .
        # . . . .

        [4, 5, 6, 10]
        # . . . .
        # X X X .
        # . . X .
        # . . . .
    ],

    # J-shape
    [
        [1, 2, 6, 10],
        # . X X .
        # . . X .
        # . . X .
        # . . . .

        [5, 6, 7, 9],
        # . . . .
        # . X X X
        # . X . .
        # . . . .

        [2, 6, 10, 11],
        # . . X .
        # . . X .
        # . X X .
        # . . . .

        [3, 5, 6, 7]
        # . . . .
        # X X X .
        # . . X .
        # . . . .
    ],

    # T-shape
    [
        [1, 4, 5, 6],
        # . X . .
        # X X X .
        # . . . .
        # . . . .

        [1, 4, 5, 9],
        # . X . .
        # X X . .
        # . X . .
        # . . . .

        [4, 5, 6, 9],
        # . . . .
        # X X X .
        # . X . .
        # . . . .

        [1, 5, 6, 9]
        # . X . .
        # . X X .
        # . X . .
        # . . . .
    ],

    # 1x1 square
    [
        [1]
        # . X . .
        # . . . .
        # . . . .
        # . . . .
    ],

    # 1x2 pill
    [
        [1, 2],
        # . X X .
        # . . . .
        # . . . .
        # . . . .

        [1, 5]
        # . X . .
        # . X . .
        # . . . .
        # . . . .
    ],

    # 2x2 square
    [
        [1, 2, 5, 6]
        # . X X .
        # . X X .
        # . . . .
        # . . . .
    ],

    # 3x3 square
    [
        [0, 1, 2, 4, 5, 6, 8, 9, 10]
        # X X X .
        # X X X .
        # X X X .
        # . . . .
    ],

    # 4x4 square
    [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        # X X X X
        # X X X X
        # X X X X
        # X X X X
    ],

    # 3x3 empty square
    [
        [0, 1, 2, 4, 6, 8, 9, 10]
        # X X X .
        # X . X .
        # X X X .
        # . . . .
    ],

    # 4x4 empty square
    [
        [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]
        # X X X X
        # X . . X
        # X . . X
        # X X X X
    ]
]

SHAPE_WEIGHTS = [
    10,  # I
    10,  # Z
    10,  # S
    10,  # L
    10,  # J
    10,  # T
    5,   # 1x1
    5,   # pill
    10,  # 2x2
    3,   # 3x3
    1,   # 4x4
    3,   # 3x3 empty
    1    # 4x4 empty
]
