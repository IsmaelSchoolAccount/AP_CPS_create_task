f = False
t = True
tr = (1, -1)
br = (1, 1)
bl = (-1, 1)
tl = (-1, -1)
c = (0, 0)
#If the corners matter (topRight, downRight, downLeft, topLeft): Which tile this is for
AUTOTILE_CORNERS = {
    (f, t, t, f): {(br, c): 0, "default": 41},
    (f, t, t, t): {(br, bl): 1, (bl, c): 33, (br, c): 34, "default": 46},
    (f, f, t, t): {(bl, c): 2, "default": 42},
    (t, t, t, t): {(tr, br, bl, tl): 12, 
                   (tr, br, bl): 4, (br, bl, tl): 5, (tr, br, tl): 11, (tr, bl, tl): 13, 
                   (bl, tl): 23, (tr, br): 31, (tr, tl): 26, (br, bl): 32, (bl, tr): 24, (br, tl): 25, 
                   (c, br): 21, (c, tl): 22, (c, tr): 29, (c, br): 30, "default": 15},
    (t, t, t, f): {(tr, br, bl, tl): 8, (tr, br, bl): 8, (tr, br, tl): 8, (tr, br): 8, 
                   (tr, bl, tl): 17, (tr, tl): 17, (tr, bl): 17, (tr, c): 17, 
                   (br, bl, tl): 28, (br, tl): 28, (br, bl): 28, (br, c): 28, "default": 27},
    (t, f, t, t): {(tr, br, bl, tl): 9, (tr, br, tl): 9, (tr, br, bl): 9, (tl, bl): 9, 
                   (tr, br, tl): 35, (br, tl): 35, (tr, tl): 35, (tl, c): 35, 
                   (tr, br, bl): 36, (br, bl): 36, (tr, bl): 36, (bl, c): 36,  "default": 37},
    (t, t, f, f): {(tr, c): 18, "default": 44},
    (t, t, f, t): {(tr, br, bl, tl): 19, (tr, br, tl): 19, (tr, bl, tl): 19, (tr, tl): 19, 
                   (tr, br): 38, (tr, c): 38, (bl, tl): 39, (tl, c): 39, "default": 40},
    (t, f, f, t): {(tl, c): 20, "default": 43}
}
#if there is a tile (Up-, Right+, Down+, Left-): What Variant You want
AUTOTILE_MAP = {
    (f, t, t, f): 0,
    (f, t, t, t): 1,
    (f, f, t, t): 2,
    (f, f, t, f): 3,
    (t, f, t, f): 6,
    (f, t, f, t): 7,
    (t, t, t, f): 8,
    (t, f, t, t): 9,
    (t, f, f, f): 10,
    (t, t, t, t): 12,
    (f, t, f, f): 14,
    (f, f, f, t): 16,
    (t, t, f, f): 18, 
    (t, t, f, t): 19, 
    (t, f, f, t): 20,
    (f, f, f, f): 45,
}
#List of offsets Square to a tile for autotiling
SQUARE_OFFSET = [(0, -1), (1, 0), (0, 1), (-1, 0)]
#List of offsets Diagonal to a tile for autotiling
CORNER_OFFSET = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
#Tiles which player interacts with
PHYSICS_TILES = ["grass_tiles"]
#Tiles which can be autotiled
AUTOTILE_TILES = ["grass_tiles"]
#List of offsets around a tile for collisions (2 tile radius for bigger players)
NEIGHBOR_OFFSETS = [(-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                    (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                    (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
                    (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                    (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2)]
#These offsets are used to determine if the player is overlapping a mushroom
OVERLAP_OFFSETS = [(0, 0), (1, 0)]
#The tiles that are air or duplicates or not used in the tileset
UNCOUNTED_GRASS_TILES = [0, 4, 6, 7, 8, 9, 11, 13, 15, 17, 19, 20, 21, 24, 25, 26, 27, 31, 35, 42, 43, 44, 51, 52, 53, 60, 61, 62, 69, 70, 71, 78, 79, 80, 81]
#Player constants
PLAYER_VEL = 1
#The base path where all the images are located
BASE_IMG_PATH = ("data/images/")
#animations and the key information for loading them
ANIMATION_TYPE = {
    "idle.png": (16, True),
    "walk.png": (8, True),
    "jump.png": (6, False),
    "land.png": (6, False),
    "fall.png": (1, False),
    "inhaling.png": (8, True),
    "inhale_start.png": (12, False),
    "exhale.png": (4, False),
    "floating_fall.png": (1, False),
    "floating_flap.png": (24, False),
#animations that are loaded but are currently not in use, for future project
    "wall_hit.png": (5, False),
    "climb_back.png": (5, True),
    "crawl.png": (5, True),
    "crouch.png": (5, True),
    "death.png": (5, True),
    "down_smash.png": (5, True),
    "down_tilt.png": (5, True),
    "f_smash.png": (5, True),
    "f_tilt.png": (5, True),
    "full.png": (5, True),
    "grab.png": (5, True),
    "hit.png": (5, True),
    "inhale_float.png": (5, True),
    "jump_fall_land.png": (5, True),
    "ledge_grab.png": (5, True),
    "left_jab.png": (5, True),
    "multi_jump.png": (5, True),
    "right_hook.png": (5, True),
    "right_left_combo.png": (5, True),
    "roll_1.png": (5, True),
    "roll_2.png": (5, True),
    "shield.png": (5, True),
    "u_smash.png": (5, True),
    "u_tilt.png": (5, True),
    "wall_slide.png": (5, True),
}
#points for win message
W_START = (105, 120)
W = [(210, 360), (315, 120), (420, 360), (525, 120)]
#amount of space between lines for W
REPEAT_TIMES = 40
#Time it takes to finish sceen shake and start next line
SCREEN_SHAKE_DUR = 30
#number of particles made when it hits the edge
W_PARTICLES = 20