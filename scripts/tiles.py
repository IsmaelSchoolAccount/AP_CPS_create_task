import pygame

import json

import scripts.constants as constants
from scripts.collectables import swallowable

class Tile():
    def __init__(self, pos, type, variant):
        self.pos = list(pos)
        self.type = type
        self.variant = variant

    def copy(self):
        return Tile(self.pos.copy(), self.img.copy())

#Some of the code (init, tiles_around, physics_rects_around, and render) and the json save and load in (class Tilemap) was made publicly available by DaFluffyPotato
class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

    def autotile(self):
        for loc in self.tilemap:
            self.autotile_loc(loc)

    def autotile_loc(self, loc):
        tile = self.tilemap[loc]
        if tile.type in constants.AUTOTILE_TILES:
            neighbors = [False, False, False, False]
            for offset in constants.SQUARE_OFFSET:
                check_loc = (loc[0] + offset[0], loc[1] + offset[1])
                if check_loc in self.tilemap and self.tilemap[check_loc].type == tile.type:
                    neighbors[constants.SQUARE_OFFSET.index(offset)] = True
            neighbors = tuple(neighbors)
            if neighbors in constants.AUTOTILE_MAP:
                if neighbors in constants.AUTOTILE_CORNERS:
                    corners_vars = constants.AUTOTILE_CORNERS[neighbors]
                    for offsets in corners_vars:
                        if offsets == "default":
                            tile.variant = corners_vars["default"]
                            break
                        corner_check = True
                        for offset in offsets:
                            check_loc = (loc[0] + offset[0], loc[1] + offset[1])
                            if not check_loc in self.tilemap:
                                corner_check = False
                                break
                        if corner_check:
                            tile.variant = corners_vars[offsets]
                            break
                else:
                    tile.variant = constants.AUTOTILE_MAP[neighbors]

    def find_highest_collision_point(self, pos):
        tile_loc = self.point_to_loc(pos)
        for y in range(50):
            for x in range(2):
                if self.game.player.flip:
                    check_loc = (tile_loc[0] - 5 + x, tile_loc[1] + y)
                else:
                    check_loc = (tile_loc[0] + 4 + x, tile_loc[1] + y)
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc].type in constants.PHYSICS_TILES:
                        return self.loc_to_point((check_loc[0], check_loc[1] - 2))[1]
        return pos[1]

    def point_to_loc(self, pos):
        return (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
            
    def loc_to_point(self, loc):
        return (loc[0] * self.tile_size, loc[1] * self.tile_size)

    def tiles_around(self, pos, offsets):
        tiles = []
        tile_loc = self.point_to_loc(pos)
        for offset in offsets:
            check_loc = (tile_loc[0] + offset[0], tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos, constants.NEIGHBOR_OFFSETS):
            if tile.type in constants.PHYSICS_TILES:
                rects.append(pygame.Rect(tile.pos[0] * self.tile_size, tile.pos[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def check_win(self, pos):
        for tile in self.tiles_around(pos, constants.OVERLAP_OFFSETS):
            if tile.type == "win":
                return True
        return False

    def render(self, surface, offset=(0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = (x, y)
                if location in self.tilemap:
                    tile = self.tilemap[(x, y)]  
                    surface.blit(self.game.assets[tile.type][tile.variant], (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))  
                    
    def tile_to_dict(self, tilemap) -> dict:
        tiles = {}
        for tile in tilemap:
            tiles[str(tile[0]) + ";" + str(tile[1])] = {"type": tilemap[tile].type, "variant": tilemap[tile].variant, "pos": tilemap[tile].pos}
        return tiles
    
    def dict_to_tile(self, game, tilemap):
        tiles = {}
        for tile in tilemap:
            if tilemap[tile]["type"] == "swallows" and not self.game.editor:
                game.swallows.append(swallowable(self.game, (tilemap[tile]["pos"][0] * self.tile_size, tilemap[tile]["pos"][1] * self.tile_size), tilemap[tile]["type"], tilemap[tile]["variant"], tilemap[tile]["pos"][1]*self.tile_size))
            else:
                tiles[(tilemap[tile]["pos"][0], tilemap[tile]["pos"][1])] = Tile(tilemap[tile]["pos"], tilemap[tile]["type"], tilemap[tile]["variant"])
        return tiles
                    
    def save(self, path):
        f = open(path, "w")
        json.dump({"tile_size": 16, "tilemap": self.tile_to_dict(self.tilemap)}, f)
        f.close()

    def load(self, game, path):
        f = open(path, "r")
        map_data = json.load(f)
        f.close()

        self.tile_size = map_data["tile_size"]
        self.tilemap = self.dict_to_tile(game, map_data["tilemap"])