import pygame
import sys

def key_events_editor(self):
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking[0] = True
                    if event.button == 3:
                        self.clicking[1] = True
                    if self.e_buttons[0]:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                    else:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking[0] = False
                    if event.button == 3:
                        self.clicking[1] = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_e:
                        self.e_buttons[2] = True 
                    if event.key == pygame.K_o:
                        self.tilemap.save("map.json")
                    if event.key == pygame.K_LSHIFT:
                        self.e_buttons[0] = True
                    if event.key == pygame.K_LCTRL:
                        self.e_buttons[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_e:
                        self.e_buttons[2] = False
                    if event.key == pygame.K_LSHIFT:
                        self.e_buttons[0] = False
                    if event.key == pygame.K_LCTRL:
                        self.e_buttons[1] = False

def key_events_game(self):
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                    if event.key == pygame.K_a:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_s:
                        self.player.falling_multiplier = 2
                    if event.key == pygame.K_e:
                        self.player.inhale()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_a:
                        self.movement[1] = False
                    if event.key == pygame.K_s:
                        self.player.falling_multiplier = 1               