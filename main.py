import pygame, sys, os
from load_map import load_map
from textures import TEXTURES

pygame.display.set_caption("Undergrounder")
cmap1 = load_map('maps/cmap1')
bmap1 = load_map('maps/bmap1')
emap1 = load_map('maps/emap1')
umap1 = load_map('maps/umap1')
bmap2 = load_map('maps/bmap2')
emap2 = load_map('maps/emap2')
umap2 = load_map('maps/umap2')
WINDOW_SIZE = (1280, 720)
TILE_SIZE = 32
BOTTOMTILE_SIZE = 12
SURFACE_SIZE = (512, 288)
upper_blocks = []
bottom_blocks = []
entities = []
chunks = []

class Chunk(object):
    """Chunk class"""
    def __init__(self, pos_x, pos_y, bmap, umap, emap):
        chunks.append(self)
        #self.id = id                           # id - type of chunk's pattern
        self.pos_x = pos_x                      # X Position on a chunk map
        self.pos_y = pos_y                      # Y Position on a chunk map
        self.bmap = bmap
        self.umap = umap
        self.emap = emap
        self.start_x = pos_x * TILE_SIZE * 8
        self.start_y = pos_y * TILE_SIZE * 8
        self.bottom_blocks = []
        self.upper_blocks = []
        self.entities = []
        
    def create_bottom_blocks(self):
        """Create objects of Bottom class and associates them to particular chunk"""
        map_y = 0
        for row in self.bmap:
            map_x = 0
            for tile in row:
                if tile == '1':     Bottom((self.start_x + map_x * TILE_SIZE, self.start_y + map_y * TILE_SIZE), '1', self, False)
                elif tile == '2':   pass
                elif tile == '3':   Bottom((self.start_x + map_x * TILE_SIZE, self.start_y + map_y * TILE_SIZE), '3', self, True)
                elif tile == '4':   Bottom((self.start_x + map_x * TILE_SIZE, self.start_y + map_y * TILE_SIZE), '4', self, False)

                map_x += 1
            map_y += 1
            
    def create_upper_blocks(self):
        """Create objects of Barrier class and associates them to particular chunk"""
        map_y = 0
        for row in self.umap:
            map_x = 0
            for tile in row:
                if tile == '1':     Barrier((self.start_x + map_x * TILE_SIZE, self.start_y + map_y * TILE_SIZE), '1', self)
                elif tile == '2':   pass
                elif tile == '3':   Barrier((self.start_x + map_x * TILE_SIZE, self.start_y + map_y * TILE_SIZE), '3', self)
                elif tile == '4':   Barrier((self.start_x + map_x * TILE_SIZE, self.start_y + map_y * TILE_SIZE), '4', self)

                map_x += 1
            map_y += 1 

class Bottom(object):
    def __init__(self, pos, id, Chunk, imp):
        # imp(bool) - True: object is impassable
        Chunk.bottom_blocks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.id = id
        self.imp = imp

class Barrier(object):
    """Impassable object class"""
    def __init__(self, pos, id, Chunk):
        Chunk.upper_blocks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
        self.id = id

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

        for chunk in chunks:
            for barrier in chunk.upper_blocks:
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
        self.mouse_x = None
        self.mouse_y = None
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
            
    def load_fonts(self):
        """load all fonts"""
        self.fonts = {
            'font1': pygame.font.Font('fonts/rainyhearts.ttf', 16)
        }
    
    def create_chunk_map(self, cmap):
        """Create objects of Chunk class from cmap(chunk map)"""
        map_y = 0
        for row in cmap:
            map_x = 0
            for tile in row:
                if tile == '1':     Chunk(map_x, map_y, bmap1, umap1, emap1)
                elif tile == '2':   Chunk(map_x, map_y, bmap2, umap2, emap2)

                map_x += 1
            map_y += 1
    
    def app_event(self, player):
        '''checks if event happened'''
        self.mouse_x = pygame.mouse.get_pos()[0] - self.camera_x - int(SURFACE_SIZE[0] / 2)
        self.mouse_y = pygame.mouse.get_pos()[1] + self.camera_y - int(SURFACE_SIZE[1] / 2)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(self.mouse_x, self.mouse_y)

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
        """render single rect texture"""
        self.display.blit(texture_name, (
                        x - self.camera_x,
                        y - self.camera_y
                    ))

    def render_bottom_map(self):
        """render bottom level of rects"""
        for chunk in chunks:
            for bottom in chunk.bottom_blocks:
                if bottom.id == '1': self.render_texture(TEXTURES['dirt'], bottom.rect.x, bottom.rect.y)  
                elif bottom.id == '2': pass
                elif bottom.id == '3': self.render_texture(TEXTURES['obsidian'], bottom.rect.x, bottom.rect.y)
                elif bottom.id == '4': self.render_texture(TEXTURES['stone'], bottom.rect.x , bottom.rect.y)
 
    def render_upper_map(self):
        """render upper level of rects"""
        for chunk in chunks:
            for upper in chunk.upper_blocks:
                if upper.id == '1':     self.render_texture(TEXTURES['dirt'], upper.rect.x, upper.rect.y - BOTTOMTILE_SIZE)  
                elif upper.id == '2':   pass
                elif upper.id == '3':   self.render_texture(TEXTURES['obsidian'], upper.rect.x, upper.rect.y - BOTTOMTILE_SIZE)
                elif upper.id == '4':   self.render_texture(TEXTURES['stone'], upper.rect.x, upper.rect.y - BOTTOMTILE_SIZE)
                
    def render_entities(self):
        """render entities and player"""
        for entity in entities:
            if entity.id == '5': self.render_texture(
                TEXTURES['deer'], entity.rect.x / TILE_SIZE, entity.rect.y / TILE_SIZE)
            elif entity.id == '6': self.render_texture(
                TEXTURES['bush'], entity.rect.x / TILE_SIZE, entity.rect.y / TILE_SIZE)

    def render_player_entity_collision(self, player):
        """render entities and player when occurs any collision between them"""
        if player.rect.bottom > entities[player.rect.collidelist(entities)].rect.bottom - 2:
            self.render_entities()
            self.render_player_texture(player)
        else:
            self.render_player_texture(player)
            self.render_entities()

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

        player = Player()                                               # Create Player object
        self.load_fonts()                                               # Load fonts
        self.create_chunk_map(cmap1)                                    # Create Chunk objects from cmap
        for chunk in chunks:
            chunk.create_bottom_blocks()                                # Create Bottom objects chunk after chunk
            chunk.create_upper_blocks()                                 # Create Barrier objects chunk after chunk
        for chunk in chunks:                                            # Loop for testing
            pass
        
        while (self.running):
            self.display.fill(self.background_color)                    # Fill display with background color
            self.update_camera_position(player)                         # Update position of camera in relation to the player
            self.app_event(player)                                      # Handles events
            self.render_bottom_map()                                    # Render objects of bottom layer
            
            if not player.rect.collidelistall(entities):
                #player do not collide with any entities
                self.render_player_texture(player)
                self.render_entities()
            else:
                #player collides with at least one of entities
                self.render_player_entity_collision(player)
            
            self.render_upper_map()                                     # Render objects of upper layer
            self.render_player_coords(player)                           # Render player's coordinates
            self.render_fps_value()                                     # Render current FPS value

            surf = pygame.transform.scale(                              # Scale display to window size
                self.display, 
                WINDOW_SIZE
            )
            self.screen.blit(surf, (0,0))                   
            pygame.display.flip()                                       # Refresh display
            self.clock.tick(60)

        self.cleanup()


if __name__ == "__main__":
    App = App()
    App.app_execute()

