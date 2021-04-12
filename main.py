import pygame, sys, os
from load_map import load_map
from textures import TEXTURES

pygame.display.set_caption("Undergrounder")
game_map1 = load_map('maps/map1')
entities_map1 = load_map('maps/entities1')
upper_map1 = load_map('maps/uppermap1')
WINDOW_SIZE = (1600, 900)
TILE_SIZE = 16
SURFACE_SIZE = (320, 180)
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
        self.speed = 1

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
        self.background_color = (137,182,238)
        self.clock = pygame.time.Clock()
        self.camera_x = 0
        self.camera_y = 0
        self.fonts = None
    
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
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            player.move(-player.speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.move(player.speed, 0)
        if key[pygame.K_UP] or key[pygame.K_w]:
            player.move(0, -player.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            player.move(0, player.speed)
        if key[pygame.K_LSHIFT]:
            player.speed = 2
        else: player.speed = 1

    def load_fonts(self):
        """load all fonts"""
        self.fonts = {
            'font1': pygame.font.Font('fonts/rainyhearts.ttf', 16)
        }
        
    def render_player_coords(self, player):
        """show coordinates of a player character"""
        self.display.blit(
                self.fonts['font1'].render(str(int(player.rect.x + TILE_SIZE / 2)) + ' ' + str(int(player.rect.y + TILE_SIZE / 2)), True, (0, 0, 0)),
                (0, 0)
            )

    def render_player_texture(self, player):
        self.display.blit(
            TEXTURES['character'], 
            (player.rect.x - self.camera_x, player.rect.y - self.camera_y)
        )

    def render_texture(self, texture_name, x, y):
        """render single texture for app_render_map and app_render_entitie func"""
        self.display.blit(texture_name, (
                        x * TILE_SIZE - self.camera_x,
                        y * TILE_SIZE - self.camera_y
                    ))

    def app_render_bottom_map(self, rmap):
        """render bottom level of a map, rmap <- map to render"""
         
        map_y = 0
        for row in rmap:
            map_x = 0   
            for tile in row:
                if tile == '1': self.render_texture(TEXTURES['dirt'], map_x, map_y)  
                elif tile == '2': self.render_texture(TEXTURES['water'], map_x, map_y)
                elif tile == '3': self.render_texture(TEXTURES['barrier'], map_x, map_y)
                elif tile == '4': self.render_texture(TEXTURES['stone'], map_x, map_y)
                
                map_x += 1
            map_y += 1

    def app_render_upper_map(self, umap):
        """render upper level of a map, umap <- map to render"""
        map_y = 0
        for row in umap:
            map_x = 0   
            for tile in row:
                if tile == '1': self.render_texture(TEXTURES['dirt'], map_x, map_y - 1/4)  
                elif tile == '2': self.render_texture(TEXTURES['water'], map_x, map_y - 1/4)
                elif tile == '3': self.render_texture(TEXTURES['barrier'], map_x, map_y - 1/4)
                elif tile == '4': self.render_texture(TEXTURES['stone'], map_x, map_y - 1/4)
                
                map_x += 1
            map_y += 1

    def app_render_entities(self, emap):
        """render entities, emap <- entities map to render entities from"""
        map_y = 0
        for row in emap:
            map_x = 0
            for tile in row:
                if tile == '5': self.render_texture(TEXTURES['berry'], map_x, map_y)

                map_x +=1
            map_y += 1

    def app_create_barriers(self, bmap, umap):
        """Create barriers across the map, bamp <- bottom lvl map, umap <- upper lvl map"""
        map_y = 0
        for row in bmap:
            map_x = 0   
            for tile in row:
                if tile == '2': Barrier((map_x * TILE_SIZE, map_y * TILE_SIZE))
                if tile == '3': Barrier((map_x * TILE_SIZE, map_y * TILE_SIZE))

                map_x += 1
            map_y += 1

        map_y = 0
        for row in umap:
            map_x = 0   
            for tile in row:
                if tile != '0': Barrier((map_x * TILE_SIZE, map_y * TILE_SIZE))

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
        self.app_create_barriers(game_map1, upper_map1)
        self.load_fonts()
        
        while (self.running):
            
            self.display.fill(self.background_color)
            self.update_camera_position(player)
            self.app_event(player)
            self.app_render_bottom_map(game_map1)
            self.app_render_entities(entities_map1)
            self.render_player_texture(player)
            self.render_player_coords(player)
            self.app_render_upper_map(upper_map1)
            

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

