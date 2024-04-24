import pygame

class swallow_cone:
    def __init__(self, size):
        self.cone = {
            ((size, size * -1.5), (0, 0)): pygame.Rect(0, 0, size, size),
            ((size * 2, size * -4), (-size/2, -size/2)): pygame.Rect(0, 0, size * 2.5, size * 2)
        }

    def update(self, player):
        for rect_offset in self.cone:
            rect = self.cone[rect_offset]
            rect.x = player.pos[0] + rect_offset[0][player.flip]
            rect.y = player.pos[1] + rect_offset[1][player.flip]

    def inhale(self, game):
        for swallowable in game.swallows:
            for rect_offset in self.cone:
                if swallowable.rect().colliderect(self.cone[rect_offset]):
                    swallowable.swallowing = True

    def render(self, surf, offset=(0, 0)):
        for rect_offset in self.cone:
            rect = self.cone[rect_offset]
            surf.blit(pygame.surface.Surface(rect.size), (rect.x - offset[0], rect.y - offset[1]))