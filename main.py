import pygame, sys, os
from load_map import load_map
from textures import TEXTURES

pygame.display.set_caption("Undergrounder")
bmap1 = load_map('maps/map1')
emap1 = load_map('maps/entities1')
umap1 = load_map('maps/uppermap1')
WINDOW_SIZE = (1280, 720)
TILE_SIZE = 32
BOTTOMTILE_SIZE = 12
SURFACE_SIZE = (512, 288)
impassable_blocks = []
entities = []


class Player(object):
    """Player class"""
    def __init__(self):
        self.rect = pygame.Rect(
            4 * TILE_SIZE, 
            4 * TILE_SIZE, 
            TILE_SIZE,
            TILE_SIZE
        )
        self.INITIAL_SPEED = 2
        self.speed = self.INITIAL_SPEED
        self.left = False
        self.right = False

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

class Entity(object):
    """Entity object: bushes, chests etc."""
    def __init__(self, pos, id):
        entities.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.id = id


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
            #player.left = True
        else:
            player.left = False
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.move(player.speed, 0)
            #player.right = True
        else:
            player.right = False
        if key[pygame.K_UP] or key[pygame.K_w]:
            player.move(0, -player.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            player.move(0, player.speed)
        if key[pygame.K_LSHIFT]:
            player.speed = 2 * player.INITIAL_SPEED
        else: 
            player.speed = player.INITIAL_SPEED
            
    def load_fonts(self):
        """load all fonts"""
        self.fonts = {
            'font1': pygame.font.Font('fonts/rainyhearts.ttf', 16)
        }
        
    def render_player_coords(self, player):
        """show coordinates of a player character"""
        self.display.blit(
            self.fonts['font1'].render(str(int(player.rect.center[0])) + ' ' + str(int(player.rect.center[1])), True, (0, 0, 0)),
            (0, 0)
            )

    def render_fps_value(self):
        self.display.blit(
            self.fonts['font1'].render(str(int(self.clock.get_fps())), True, (255, 0, 0)),
            (495,0)
        )

    def render_player_texture(self, player):
        if player.left:
            self.display.blit(
                TEXTURES['character_left1'], 
                (player.rect.x - self.camera_x, player.rect.y - self.camera_y)
            )
        elif player.right:
            self.display.blit(
                TEXTURES['character_right1'], 
                (player.rect.x - self.camera_x, player.rect.y - self.camera_y)
            )
        else:
            self.display.blit(
                TEXTURES['character_front'], 
                (player.rect.x - self.camera_x, player.rect.y - self.camera_y)
            )

    def render_texture(self, texture_name, x, y):
        """render single texture for app_render_map and app_render_entitie func"""
        self.display.blit(texture_name, (
                        x * TILE_SIZE - self.camera_x,
                        y * TILE_SIZE - self.camera_y
                    ))

    def render_bottom_map(self, rmap):
        """render bottom level of a map, rmap <- map to render"""
        map_y = 0
        for row in rmap:
            map_x = 0   
            for tile in row:
                if tile == '1': self.render_texture(TEXTURES['dirt'], map_x, map_y)  
                elif tile == '2': self.render_texture(TEXTURES['water'], map_x, map_y)
                elif tile == '3': self.render_texture(TEXTURES['obsidian'], map_x, map_y)
                elif tile == '4': self.render_texture(TEXTURES['stone'], map_x, map_y)
                
                map_x += 1
            map_y += 1

    def render_upper_map(self, umap):
        """render upper level of a map, umap <- map to render"""
        map_y = 0
        for row in umap:
            map_x = 0   
            for tile in row:
                if tile == '1':     self.render_texture(TEXTURES['dirt'], map_x, map_y - BOTTOMTILE_SIZE/TILE_SIZE)  
                elif tile == '2':   self.render_texture(TEXTURES['water'], map_x, map_y - BOTTOMTILE_SIZE/TILE_SIZE)
                elif tile == '3':   self.render_texture(TEXTURES['obsidian'], map_x, map_y - BOTTOMTILE_SIZE/TILE_SIZE)
                elif tile == '4':   self.render_texture(TEXTURES['stone'], map_x, map_y - BOTTOMTILE_SIZE/TILE_SIZE)
                
                map_x += 1
            map_y += 1

    def render_entities(self):
        """render entities and player"""
        for entity in entities:
            if entity.id == '5': self.render_texture(
                TEXTURES['deer'], entity.rect.x / TILE_SIZE, entity.rect.y / TILE_SIZE)
            elif entity.id == '6': self.render_texture(
                TEXTURES['bush'], entity.rect.x / TILE_SIZE, entity.rect.y / TILE_SIZE)

    def render_player_entity_collision(self, player):
        """render entities and player when occurs any collision between them"""
        if player.rect.bottom > entities[player.rect.collidelist(entities)].rect.bottom:
            self.render_entities()
            self.render_player_texture(player)
        else:
            self.render_player_texture(player)
            self.render_entities()

    def create_barriers(self, bmap, umap):
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

    def create_entities(self, emap):
        '''create entities across the map, emap <- map of entities to create entities from'''
        map_y = 0
        for row in emap:
            map_x = 0   
            for tile in row:
                if tile == '5': Entity((map_x * TILE_SIZE, map_y * TILE_SIZE), '5')
                if tile == '6': Entity((map_x * TILE_SIZE, map_y * TILE_SIZE), '6')

                map_x += 1
            map_y += 1
            
    def update_camera_position(self, player):
        '''update camera when a character is moving'''
        self.camera_x += (player.rect.center[0] - self.camera_x - int(SURFACE_SIZE[0] / 2))
        self.camera_y += (player.rect.center[1] - self.camera_y - int(SURFACE_SIZE[1] / 2))
    
    def cleanup(self):
        '''quits all PyGame modules'''
        pygame.quit()
        sys.exit()

    def app_execute(self):
        '''main execute function'''
        if self.app_init() == False:
            self.running = False

        player = Player()
        self.create_barriers(bmap1, umap1)
        self.create_entities(emap1)
        self.load_fonts()
        
        while (self.running):
            self.display.fill(self.background_color)
            self.update_camera_position(player)
            self.app_event(player)
            self.render_bottom_map(bmap1)

            if not player.rect.collidelistall(entities):
                '''player do not collide with any entities'''
                self.render_player_texture(player)
                self.render_entities()
            else:
                '''player collides with at least one of entities'''
                self.render_player_entity_collision(player)

            self.render_upper_map(umap1)
            self.render_player_coords(player)
            self.render_fps_value()

            surf = pygame.transform.scale(
                self.display, 
                WINDOW_SIZE
            )
            self.screen.blit(surf, (0,0))
            pygame.display.flip()
            self.clock.tick(60)

        self.cleanup()


if __name__ == "__main__":
    App = App()
    App.app_execute()

