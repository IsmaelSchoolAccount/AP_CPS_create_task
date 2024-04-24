import pygame, random, math
from scripts.particles import swallow_particle, physics_particle
from scripts.abilities import swallow_cone
from scripts.collectables import swallowable

#This code (class PhysicsEntity) was made publicly available by DaFluffyPotato
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.last_vel = (0, 0)
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-26, -32)
        self.flip = False
        self.set_action("idle")

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "_animations"][self.action + ".png"].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement

        self.last_vel = self.velocity
        
        self.velocity[0] = self.velocity[0] + movement[0] * 0.1
        self.velocity[0] *= 0.9
        
        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = 0
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
    
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        #surf.blit(pygame.transform.flip(pygame.surface.Surface(self.size), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

#The basic functions (init, update, jump) of this code (class Player) was made publicly available by DaFluffyPotato
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.swallow_cone = swallow_cone(self.size[1])
        self.jumps = 0
        self.in_air = 0
        self.wall_slide = False
        self.wall_jump = False
        self.full = -1
        self.falling_multiplier = 1

    def update(self, tilemap, movement=(0, 0)):
        
        super().update(tilemap, movement=movement)

        if self.collisions['down']:
            self.in_air = 0
            self.wall_jump = False
            if self.full == 0:
                self.jumps = 3
                self.velocity[0] = 0
            else:
                self.jumps = 1

        if self.full != -1:
            self.velocity[1] = min(2 * self.falling_multiplier, self.velocity[1] + 0.05 * self.falling_multiplier)
            if self.in_air > 500:
                self.game.game_state = "dead"
        else:
            self.velocity[1] = min(5 * self.falling_multiplier, self.velocity[1] + 0.1)
            if self.in_air > 150:
                self.game.game_state = "dead"

        self.swallow_cone.update(self)
    
        if (self.collisions["right"] or self.collisions["left"]) and self.in_air >= 20:
            self.wall_slide = True
            self.jumps = 0
            self.in_air = 0
            self.wall_jump = False

        if not (self.collisions["right"] or self.collisions["left"]) or self.collisions["down"]:
            self.wall_slide = False
        
        if self.action == "exhale" and not self.animation.done:
            pass
        elif self.full != -1:
            if self.in_air > 7:
                if self.velocity[1] < 0:
                    self.set_action("floating_flap")
                else:
                    self.set_action('floating_fall')
            elif self.wall_slide or abs(self.velocity[0]) > 0.05:
                self.exhale()
            else:
                self.set_action("full")
        elif self.wall_slide:
            self.velocity[1] = min(0.5, self.velocity[1] + 0.2)
            self.set_action("wall_slide")
        elif self.last_vel[1] > 3 and self.collisions['down'] or not self.animation.done and self.action == "land": 
            self.set_action("land")
        elif self.velocity[1] < 0 or self.in_air > 20 and self.velocity[1] < 1:
            self.set_action('jump')
        elif self.velocity[1] > 0.4:
            self.set_action('fall')
        elif abs(movement[0]) > 0 and self.in_air < 5:
            self.set_action('walk')
        elif self.action == "inhale_start":
            angle = random.random() * math.pi * 2
            if self.flip:
                self.game.particles.append(swallow_particle((self.pos[0] - 32 - 1.5 * self.animation.frame * random.random() + math.sin(angle) * random.random() * self.animation.frame, self.pos[1] + 5 + math.cos(angle) * random.random() * self.animation.frame), (self.animation.frame * 0.02, 3), random.random() + 0.5, -math.cos(angle)/2))
            else:
                self.game.particles.append(swallow_particle((self.pos[0] + 32 + 1.5 * self.animation.frame * random.random() + math.sin(angle) * random.random() * self.animation.frame, self.pos[1] + 5 + math.cos(angle) * random.random() * self.animation.frame), (self.animation.frame * -0.02, 3), random.random() + 0.5, -math.cos(angle)/2))
            if self.animation.done:
                self.set_action("inhaling")
        elif self.action == "inhaling":
            self.swallow_cone.inhale(self.game)
            angle = random.random() * math.pi * 2
            if self.flip:
                self.game.particles.append(swallow_particle((self.pos[0] - 78 + math.sin(angle) * random.random() * 50, self.pos[1] + 5 + math.cos(angle) * random.random() * 50), (0.75, 5), random.random() + 1, -math.cos(angle)))
            else:
                self.game.particles.append(swallow_particle((self.pos[0] + 96 + math.sin(angle) * random.random() * 50, self.pos[1] + 5 + math.cos(angle) * random.random() * 50), (-0.75, 5), random.random() + 1, -math.cos(angle)))
        else:
            self.set_action('idle')

        self.in_air += 1
        
    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset=offset)
        #self.swallow_cone.render(surface, offset)

    def jump(self):
        if self.jumps:
            if self.full != -1:
                if self.in_air > 20:
                    if self.action == "floating_fall" or self.action == "full":
                        self.velocity[1] = -2
                        self.jumps -= 1
                        if self.flip:
                            self.velocity[0] = -1.5
                        else:
                            self.velocity[0] = 1.5
                else:
                    self.velocity[1] = -2
                    self.jumps -= 1
                    self.in_air = 8
            else:
                self.velocity[1] = -3
                self.jumps -= 1
        elif self.wall_slide:
            self.wall_jump = True
            self.velocity[1] = -3
            if self.flip:
                self.velocity[0] = 8
            else:
                self.velocity[0] = -8
    
    def inhale(self):
        if self.action == "idle":
            self.set_action("inhale_start")
        if self.full != -1:
            self.exhale()

    def exhale(self):
        self.set_action("exhale")
        if self.flip:
            vel = (-12, 0)
            for i in range(20):
                self.game.particles.append(physics_particle((self.pos[0] - self.size[0] * 2, self.pos[1]), ((-random.random() - 0.5) * 2, (random.random() - 0.2) * -2), random.random() + 1))
        else:
            vel = (12, 0)
            for i in range(20):
                self.game.particles.append(physics_particle((self.pos[0] + self.size[0] * 2, self.pos[1]), ((random.random() + 0.5 ) * 3, (random.random() - 0.2) * -2), random.random() + 1))
        self.game.swallows.append(swallowable(self.game, (self.pos[0] - self.size[0], self.pos[1] - self.size[1]), 0, self.full, vel=vel, target_y=self.game.tilemap.find_highest_collision_point(self.rect().center)))
        self.full = -1
        self.in_air = 5


