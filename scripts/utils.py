import pygame

import os
import scripts.constants as constants

#The load_image function was made publicly available by DaFluffyPotato
def load_image(path):
    img = pygame.image.load(constants.BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_tile_sheet(path, start=(0, 0), area=(1, 1), remove=[], tile_size=16):
    sprite_sheet = load_image(path)

    tiles = []
    
    idx = 0
    for i in range(area[1]):
        for j in range(area[0]):
            if idx not in remove:
                surface = pygame.Surface((tile_size, tile_size))
                rect = pygame.Rect((start[0] + j) * tile_size, (start[1] + i) * tile_size, tile_size, tile_size)
                surface.blit(sprite_sheet, (0, 0), rect)
                surface.set_colorkey((0, 0, 0))
                tiles.append(surface)
            idx += 1
    return tiles

def load_animations(path, img_name, tile_size=16, entity_size=(64, 64)):
    animation = load_image(path)
    frames = []
    for i in range(animation.get_width() // tile_size):
        surface = pygame.Surface(entity_size)
        rect = pygame.Rect((i * tile_size, 0), entity_size)
        surface.blit(animation, (0, 0), rect)
        surface.set_colorkey((0, 0, 0))
        frames.append(surface)
    return Animation(frames, constants.ANIMATION_TYPE[img_name][0], constants.ANIMATION_TYPE[img_name][1])

def load_all_animations(path, tile_size=16, entity_size=(64, 64)):
    animations = {}
    for img_name in sorted(os.listdir(constants.BASE_IMG_PATH + path)):
        animations[img_name] = load_animations(path + '/' + img_name, img_name, tile_size, entity_size)
    return animations

#The load_images function was made publicly available by DaFluffyPotato
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(constants.BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

#The animation class was made publicly available by DaFluffyPotato
class Animation:
    def __init__(self, images, img_dur=12, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    
    