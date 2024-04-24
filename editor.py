import pygame
import sys
from scripts.utils import load_tile_sheet, load_image
from scripts.tiles import Tilemap, Tile
from scripts.event_handler import key_events_editor
import scripts.constants as constants

RENDER_SCALE = 2.0

#Some of the basic functionality of the editor was made publicly available by DaFluffyPotato
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Map Editor")
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480))

        self.clock = pygame.time.Clock()
        self.editor = True

        self.assets = {
                "grass_tiles": load_tile_sheet(path="tileset.png", area=(9, 9), remove=constants.UNCOUNTED_GRASS_TILES),
                "swallows": [load_image("swallows/swallow_cloud.png")],
                "win": load_tile_sheet(path="tileset.png", start=(11, 7))
        }

        self.tilemap = Tilemap(self)

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.scroll = [0, 0]
        self.movement = [False, False, False, False]
        #Clicking = [Left Click, Right Click]
        self.clicking = [False, False]
        #E_Buttons = [Shift, Ctrl, e]
        self.e_buttons = [False, False, False]
        
        try:
            self.tilemap.load(self, "map.json")
        except FileNotFoundError:
            pass
    
    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            key_events_editor(self)

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 8
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 8
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.clicking[0]:
                self.tilemap.tilemap[tile_pos] = Tile(tile_pos, self.tile_list[self.tile_group], self.tile_variant)
            if tile_pos in self.tilemap.tilemap:
                if self.clicking[1]:
                    del self.tilemap.tilemap[tile_pos]
                if self.e_buttons[2]:
                    self.tile_variant = self.tilemap.tilemap[tile_pos].variant
                    self.tile_group = self.tile_list.index(self.tilemap.tilemap[tile_pos].type)
                
            self.tilemap.render(self.display, render_scroll)
            self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            self.display.blit(current_tile_img, (10, 10))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()