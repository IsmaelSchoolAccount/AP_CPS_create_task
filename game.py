import random
import pygame
from scripts.particles import physics_particle
from scripts.utils import load_tile_sheet, load_image, load_images, load_all_animations
from scripts.tiles import Tilemap
from scripts.clouds import Clouds
from scripts.entities import Player
from scripts.event_handler import key_events_game
import scripts.constants as constants

#A lot of this code was inspired a video
#https://www.youtube.com/watch?v=2gABYM5M0ww
#By: DaFluffyPotato
#I have kept many of the things from the tutorial including:
    #The clouds in the background (completely unchanged)
    #The class for a physics entity (completely unchanged)
    #The class for animations (completely unchanged)
    #The very basics of the tilemap class (Does not include the Tile Class which I made myself and had to change the whole thing to make it work)
    #The functions for importing images (I had to make my own of these as well because of the variety of different ways pixel art is made available (spritesheets, files, sperated sprite sheets))
    #And finally the Game class takes a lot of the structure of the platformer
#Also the particle system was inspired by another video:
#https://www.youtube.com/watch?v=F69-t33e8tk
#However I have made many changes to these and have made the rest of this code on my own
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Platformer")
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480))

        self.clock = pygame.time.Clock()
        self.editor = False

        self.assets = {
            "background": pygame.transform.scale2x(load_image("background.png")),
            'clouds': load_images('clouds'),
            "grass_tiles": load_tile_sheet(path="tileset.png", area=(9, 9), remove=constants.UNCOUNTED_GRASS_TILES),
            "player_animations": load_all_animations("spritesheets", tile_size=64),
            "swallows": [load_image("swallows/swallow_cloud.png")],
            "win": load_tile_sheet(path="tileset.png", start=(11, 7))
        }
        
        #self.sfx = {}
        self.clouds = Clouds(self.assets['clouds'], count=24)

    def load_map(self, path):
        self.player = Player(self, (0, 0), (12, 16))

        self.tilemap = Tilemap(self)
        
        self.frame = 0
    
        self.particles = []
        self.swallows = []

        self.scroll = [0, 0]
        self.movement = [False, False]

        self.tilemap.load(self, path + ".json")

        self.game_state = "run"
        
    def run(self, map):
        self.load_map(map)
        while self.game_state == "run":
              self.game_loop()
        if self.game_state == "dead":
            self.run("map")
        if self.game_state == "win":
            self.win()

    def game_loop(self):
            self.display.blit(self.assets["background"], (0, 0)) 
            self.frame += 1

            key_events_game(self)
            
            self.player.update(self.tilemap, movement=(constants.PLAYER_VEL * (self.movement[0] - self.movement[1]), 0))
            self.clouds.update()
            if self.tilemap.check_win(self.player.pos):
                self.game_state = "win"
                
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 20
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.render(self.display, render_scroll)
            self.tilemap.render(self.display, render_scroll)
            for swallowable in self.swallows:
                swallowable.update()
                if swallowable.swallowed:
                    self.player.full = swallowable.variant
                    self.swallows.remove(swallowable)
                swallowable.render(self.display, render_scroll)
            self.player.render(self.display, render_scroll)

            for particle in self.particles:
                particle.update()
                if particle.frame <= 0:
                    self.particles.remove(particle)
                else:
                    particle.render(self.display, render_scroll)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def win(self):
        self.clock.tick(10)
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        self.clock.tick(10)
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()
        self.clock.tick(2)
        pygame.display.update()
        self.draw()

    def draw(self):
        brush_size = (20, 20)
        final_display = pygame.surface.Surface((640, 480)) 
        last_point = constants.W_START
        for point in constants.W:
            offset = (point[0] - last_point[0], point[1] - last_point[1])
            screen_shake = 0
            for point_repeat in range(constants.REPEAT_TIMES):
                adjusted_points = (point[0] - offset[0]/constants.REPEAT_TIMES * point_repeat, point[1] - offset[1]/constants.REPEAT_TIMES * point_repeat)
                win_screen = pygame.surface.Surface((brush_size[0] + adjusted_points[0], brush_size[1] + adjusted_points[1]))
                black_screen_x = pygame.surface.Surface((adjusted_points[0] + brush_size[0], adjusted_points[1]))
                black_screen_y = pygame.surface.Surface((adjusted_points[0], adjusted_points[1] + brush_size[1]))
                win_screen.blit(self.display, (0, 0))
                win_screen.blit(black_screen_x, (0, 0))
                win_screen.blit(black_screen_y, (0, 0))
                win_screen.set_colorkey((0, 0, 0))
                final_display.blit(win_screen, (0, 0))
                render_pos = [0, 0]
                if point_repeat > constants.REPEAT_TIMES*9/10:
                    screen_shake += 3
                render_pos[0] = (random.randint(0, 8) - 4) * screen_shake/4
                render_pos[1] = (random.randint(0, 8) - 4) * screen_shake/4
                self.screen.blit(pygame.transform.scale(final_display, self.screen.get_size()), render_pos)
                pygame.display.update()
                self.clock.tick(60)
            self.particles.clear()
            for i in range(constants.W_PARTICLES):
                if last_point[1] > point[1]:
                    self.particles.append(physics_particle(last_point, ((random.random() - 0.5) * 10, random.random() * 10), random.random() + 1))
                else:
                    self.particles.append(physics_particle(last_point, ((random.random() - 0.5) * 5, (random.random() - 0.2) * -5), random.random() + 1))
            screen_shake = 20
            for screen_shake_repeat in range(constants.SCREEN_SHAKE_DUR):
                screen_shake -= 0.2
                render_pos[0] = (random.randint(0, 8) - 4) * screen_shake/4
                render_pos[1] = (random.randint(0, 8) - 4) * screen_shake/4
                particle_display = pygame.surface.Surface((640, 480))
                particle_display.blit(final_display, (0, 0))
                for particle in self.particles:
                    particle.update()
                    if particle.frame <= 0:
                        self.particles.remove(particle)
                    else:
                        particle.render(particle_display, (0, 0))
                self.screen.blit(pygame.transform.scale(particle_display, self.screen.get_size()), render_pos)
                pygame.display.update()
                self.clock.tick(60)
            last_point = point
        self.clock.tick(0.3)
        pygame.display.update()
        
Game().run("map")