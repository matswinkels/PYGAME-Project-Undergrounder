import pygame, sys, os
from load_map import load_map

texture_stone = pygame.image.load('img/stone.png')
texture_dirt = pygame.image.load('img/dirt.png')
texture_water = pygame.image.load('img/water.png')
texture_character = pygame.image.load('img/character.png')
texture_barrier = pygame.image.load('img/barrier.png')
pygame.display.set_caption("Undergrounder")

game_map = load_map('maps/map1')

WINDOW_SIZE = (1000, 1000)
TILE_SIZE = 16
SURFACE_SIZE = (320, 320)
impassable_blocks = []


class Player(object):
    """Player class"""
    def __init__(self):
        self.rect = pygame.Rect(
            SURFACE_SIZE[0] / 2, 
            SURFACE_SIZE[0] / 2, 
            TILE_SIZE,
            TILE_SIZE
        )
        self.speed = 2

    def move(self, x, y):
        if x != 0: self.move_on_axis(x, 0)
        if y != 0: self.move_on_axis(0, y)

    def move_on_axis(self, x, y):
        self.rect.x += x
        self.rect.y += y

        for barrier in impassable_blocks:
            if self.rect.colliderect(barrier):
                if x > 0: self.rect.right = barrier.rect.left
                if x < 0: self.rect.left = barrier.rect.right
                if y > 0: self.rect.bottom = barrier.rect.top
                if y < 0: self.rect.top = barrier.rect.bottom

class Barrier(object):
    """Impassable object class"""
    def __init__(self, pos):
        impassable_blocks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)

class App(object):
    """Game class"""
    def __init__(self):
        # GAME PROPERTIES
        self.running = True
        self.screen = None
        self.display = None
        self.background_color = (200,200,200)
        self.clock = pygame.time.Clock()
        self.camera_x = 0
        self.camera_y = 0
    
    def app_init(self):
        '''initialize all PyGame modules, create main display and 
        try to use hardware acceleration'''
        pygame.init()
        self.screen = pygame.display.set_mode(
            WINDOW_SIZE, 
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.display = pygame.Surface(SURFACE_SIZE)
        self.running = True

    def app_event(self, player):
        '''checks if event happened'''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-player.speed, 0)
        if key[pygame.K_RIGHT]:
            player.move(player.speed, 0)
        if key[pygame.K_UP]:
            player.move(0, -player.speed)
        if key[pygame.K_DOWN]:
            player.move(0, player.speed)
      
    def render_texture(self, texture_name, x, y):
        """render single texture for app_render_map func"""
        self.display.blit(texture_name, (
                        x * TILE_SIZE - self.camera_x,
                        y * TILE_SIZE - self.camera_y
                    ))

    def app_render_map(self):
        """render map""" 
        map_y = 0
        for row in game_map:
            map_x = 0   
            for tile in row:
                if tile == '0':   self.render_texture(texture_stone, map_x, map_y)
                elif tile == '1': self.render_texture(texture_dirt, map_x, map_y)  
                elif tile == '2': self.render_texture(texture_water, map_x, map_y)
                elif tile == '3': self.render_texture(texture_barrier, map_x, map_y)
                
                map_x += 1
            map_y += 1

    def app_create_barriers(self):
        """Create barriers across the map"""
        map_y = 0
        for row in game_map:
            map_x = 0   
            for tile in row:
                if tile == '2': Barrier((map_x * TILE_SIZE, map_y * TILE_SIZE))
                if tile == '3': Barrier((map_x * TILE_SIZE, map_y * TILE_SIZE))

                map_x += 1
            map_y += 1

    def update_camera_position(self, player):
        '''update camera when moving with a character'''
        self.camera_x += (player.rect.x - self.camera_x - int(SURFACE_SIZE[0] / 2))
        self.camera_y += (player.rect.y - self.camera_y - int(SURFACE_SIZE[1] / 2))
    
    def app_cleanup(self):
        '''quits all PyGame modules'''
        pygame.quit()
        sys.exit()

    def app_execute(self):
        '''main execute function'''
        if self.app_init() == False:
            self.running = False

        player = Player()
        self.app_create_barriers()

        
        while (self.running):
            
            self.display.fill(self.background_color)
            self.update_camera_position(player)
            self.app_event(player)
            self.app_render_map()
            self.display.blit(texture_character, (player.rect.x - self.camera_x, player.rect.y - self.camera_y))

            surf = pygame.transform.scale(
                self.display, 
                WINDOW_SIZE
            )
            self.screen.blit(surf, (0,0))
            pygame.display.flip()
            self.clock.tick(60)


        self.app_cleanup()


if __name__ == "__main__":
    App = App()
    App.app_execute()

