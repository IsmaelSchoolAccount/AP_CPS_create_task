import pygame, math

class particle:
    def __init__(self, pos, vel, frame):
        self.pos = list(pos)
        self.vel = list(vel)
        self.frame = frame

    def update(self):
        self.frame -= 0.04

    def render(self, surface, offset=(0, 0)):
        pygame.draw.circle(surface, (255, 255, 255), (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.frame * 1.5)

class swallow_particle(particle):
    def __init__(self, pos, vel, frame, constant_y_vel=0):
        super().__init__(pos, vel, frame)
        self.constant_y_vel = constant_y_vel

    def update(self):
        super().update()
        self.pos[0] += self.vel[0] * self.frame
        self.pos[1] += math.sin(self.frame * self.vel[1]) + self.constant_y_vel

class physics_particle(particle):
    def __init__(self, pos, vel, frame):
        super().__init__(pos, vel, frame)

    def update(self):
        super().update()
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= 0.99
        self.vel[1] = min(self.vel[1] + 0.1, 5)