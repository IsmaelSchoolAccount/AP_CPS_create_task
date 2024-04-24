import pygame, math

class swallowable:
    def __init__(self, game, pos, type, variant, target_y, vel=(0, 0)):
        self.game = game
        self.vel = vel
        self.pos = list(pos)
        self.type = type
        self.variant = variant
        self.size = self.game.assets["swallows"][self.variant].get_size()
        self.target_y = target_y 
        self.swallowing = False
        self.swallowed = False

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel = (self.vel[0] * 0.85, self.vel[1] * 0.85)
        if self.swallowing:
            if self.game.player.action == "inhaling":
                if self.game.player.flip:
                    self.pos[0] -= (self.pos[0] - self.game.player.pos[0]) * 0.03
                else:
                    self.pos[0] -= (self.pos[0] - self.game.player.pos[0] + self.game.player.size[0] * 2) * 0.03
                self.pos[1] -= (self.pos[1] - self.game.player.pos[1] + self.game.player.size[1]) * 0.03
                if self.overlap(self.rect().center, self.game.player.rect().center, (4, 50)):
                    self.swallowed = True
            else:
                self.swallowing = False
        else:
            self.pos[1] -= (self.pos[1] - self.target_y) * 0.01
            #pygame.draw.circle(self.game.display, (0, 0, 0), (self.pos[0] - self.game.scroll[0], self.target_y  - self.game.scroll[1]), 2)
        self.pos[1] = math.sin(self.game.frame/25) * 0.25 + self.pos[1] 
            
    def rect(self):
        return pygame.Rect(self.pos, self.size)

    def render(self, surface, scroll=(0, 0)):
        surface.blit(self.game.assets["swallows"][self.variant], (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))        

    def overlap(self, swallow_center, player_center, swallow_box):
        return pygame.rect.Rect(player_center[0] - swallow_box[0]//2, player_center[1] - swallow_box[1]//2, swallow_box[0], swallow_box[1]).collidepoint(swallow_center)