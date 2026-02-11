
import pgzrun
import random
import math
from pygame import Rect


WIDTH = 800
HEIGHT = 600
TITLE = "Space Cat Adventure"
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE


STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_LEVEL_COMPLETE = "level_complete"
STATE_PLANET_INTRO = "planet_intro"


PLANET_NAMES = [
    "NEBULA X-7",
    "CRIMSON MARS",
    "AQUA TITAN",
    "SOLAR DESERT",
    "VOID STATION",
    "CRYSTAL MOON",
    "PLASMA WORLD",
    "DARK MATTER"
]


class AnimatedSprite:
 
    def __init__(self, grid_x, grid_y, color, size=30):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.target_x = grid_x
        self.target_y = grid_y
        self.x = grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = grid_y * CELL_SIZE + CELL_SIZE // 2
        self.color = color
        self.size = size
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.is_moving = False
        self.direction = "down"
        
    def update_position(self, dt):
       
        target_pixel_x = self.target_x * CELL_SIZE + CELL_SIZE // 2
        target_pixel_y = self.target_y * CELL_SIZE + CELL_SIZE // 2
        
        speed = 200 * dt
        dx = target_pixel_x - self.x
        dy = target_pixel_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < 2:
            self.x = target_pixel_x
            self.y = target_pixel_y
            self.grid_x = self.target_x
            self.grid_y = self.target_y
            self.is_moving = False
        else:
            self.x += (dx / distance) * speed
            self.y += (dy / distance) * speed
            self.is_moving = True
            
    def update_animation(self, dt):
      
        if self.is_moving:
            self.animation_frame += self.animation_speed
        else:
            self.animation_frame += self.animation_speed * 0.3
            
        if self.animation_frame >= 4:
            self.animation_frame = 0
            
    def can_move_to(self, grid_x, grid_y, obstacles):
      
        if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT:
            return False
        for obs in obstacles:
            if obs['x'] == grid_x and obs['y'] == grid_y:
                return False
        return True


class Player(AnimatedSprite):
 
    
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, (30, 30, 30), size=32)
        self.helmet_color = (200, 200, 255)
        
    def move(self, dx, dy, obstacles, enemies):
        """Move player if not currently moving"""
        if self.is_moving:
            return False
            
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        if self.can_move_to(new_x, new_y, obstacles):
            self.target_x = new_x
            self.target_y = new_y
            
            if dx > 0:
                self.direction = "right"
            elif dx < 0:
                self.direction = "left"
            elif dy > 0:
                self.direction = "down"
            elif dy < 0:
                self.direction = "up"
            return True
        return False
        
    def draw(self):
      
        frame_offset = int(self.animation_frame)
        breath = math.sin(self.animation_frame * 2) * 2
        
      
        body_size = self.size + (2 if frame_offset % 2 == 0 else 0)
        screen.draw.filled_circle((self.x, self.y), body_size // 2, self.color)
        
       
        leg_y = self.y + body_size // 2 - 3
        leg_offset = 8
        if self.is_moving:
            if frame_offset % 2 == 0:
                screen.draw.filled_circle((self.x - leg_offset, leg_y + 2), 4, self.color)
                screen.draw.filled_circle((self.x + leg_offset, leg_y), 4, self.color)
            else:
                screen.draw.filled_circle((self.x - leg_offset, leg_y), 4, self.color)
                screen.draw.filled_circle((self.x + leg_offset, leg_y + 2), 4, self.color)
        else:
            screen.draw.filled_circle((self.x - leg_offset, leg_y), 4, self.color)
            screen.draw.filled_circle((self.x + leg_offset, leg_y), 4, self.color)
        
      
        screen.draw.circle((self.x, self.y - 1), self.size // 2 + 2, (150, 150, 150))
        
       
        helmet_size = self.size - 2
        screen.draw.filled_circle((self.x, self.y - 2), helmet_size // 2, 
                                 (180, 200, 255, 120))
        
    
        screen.draw.filled_circle((self.x - 6, self.y - 10), 5, (255, 255, 255, 200))
        screen.draw.filled_circle((self.x - 3, self.y - 8), 3, (255, 255, 255, 150))
        
    
        eye_offset = 7
        eye_y = self.y - 3 + breath
        screen.draw.filled_circle((self.x - eye_offset, eye_y), 5, (255, 255, 120))
        screen.draw.filled_circle((self.x + eye_offset, eye_y), 5, (255, 255, 120))
        
     
        screen.draw.filled_circle((self.x - eye_offset - 1, eye_y - 1), 2, (255, 255, 200))
        screen.draw.filled_circle((self.x + eye_offset - 1, eye_y - 1), 2, (255, 255, 200))
        
       
        screen.draw.line((self.x - eye_offset, eye_y - 2), 
                        (self.x - eye_offset, eye_y + 2), (0, 0, 0))
        screen.draw.line((self.x + eye_offset, eye_y - 2), 
                        (self.x + eye_offset, eye_y + 2), (0, 0, 0))
        
      
        if not self.is_moving or frame_offset < 2:
          
            screen.draw.filled_circle((self.x - 13, self.y - 16), 6, self.color)
            screen.draw.filled_circle((self.x - 13, self.y - 15), 3, (255, 150, 150))
           
            screen.draw.filled_circle((self.x + 13, self.y - 16), 6, self.color)
            screen.draw.filled_circle((self.x + 13, self.y - 15), 3, (255, 150, 150))
        
       
        screen.draw.filled_circle((self.x, self.y + 3), 2, (255, 150, 180))
        
       
        whisker_y = self.y + 2
        screen.draw.line((self.x - 15, whisker_y), (self.x - 8, whisker_y), (200, 200, 200))
        screen.draw.line((self.x + 15, whisker_y), (self.x + 8, whisker_y), (200, 200, 200))
        screen.draw.line((self.x - 15, whisker_y - 2), (self.x - 8, whisker_y - 1), (200, 200, 200))
        screen.draw.line((self.x + 15, whisker_y - 2), (self.x + 8, whisker_y - 1), (200, 200, 200))
        
       
        tail_wave = math.sin(self.animation_frame * 3) * 3
        screen.draw.line((self.x - body_size//2, self.y + 5), 
                        (self.x - body_size//2 - 8, self.y + 10 + tail_wave), self.color)
        screen.draw.circle((self.x - body_size//2 - 8, self.y + 10 + tail_wave), 3, self.color)


class Enemy(AnimatedSprite):
   
    
    def __init__(self, grid_x, grid_y, enemy_type="green"):
        if enemy_type == "green":
            color = (100, 255, 100)
        else:
            color = (255, 150, 200)
            
        super().__init__(grid_x, grid_y, color, size=28)
        self.enemy_type = enemy_type
        self.move_timer = 0
        self.move_interval = random.uniform(1.0, 2.5)
        
    def update(self, dt, obstacles, player, other_enemies):
    
        self.update_position(dt)
        self.update_animation(dt)
        
        if not self.is_moving:
            self.move_timer += dt
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.move_interval = random.uniform(1.0, 2.5)
                self.patrol(obstacles, other_enemies)
                
    def patrol(self, obstacles, other_enemies):
     
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
          
            occupied = False
            for enemy in other_enemies:
                if enemy != self and enemy.target_x == new_x and enemy.target_y == new_y:
                    occupied = True
                    break
                    
            if not occupied and self.can_move_to(new_x, new_y, obstacles):
                self.target_x = new_x
                self.target_y = new_y
                break
                
    def draw(self):
        
        frame_offset = int(self.animation_frame)
        bob = math.sin(self.animation_frame * 3) * 3
        
  
        body_y = self.y + bob
        screen.draw.filled_circle((self.x, body_y), self.size // 2, self.color)
        
    
        segment_color = tuple(max(0, c - 30) for c in self.color)
        screen.draw.circle((self.x, body_y - 6), 6, segment_color)
        screen.draw.circle((self.x, body_y + 2), 8, segment_color)
        
      
        arm_wave = math.sin(self.animation_frame * 4) * 2
    
        screen.draw.line((self.x - 8, body_y), 
                        (self.x - 15, body_y + 8 + arm_wave), self.color)
        screen.draw.filled_circle((self.x - 15, body_y + 8 + arm_wave), 3, self.color)
     
        screen.draw.line((self.x + 8, body_y), 
                        (self.x + 15, body_y + 8 - arm_wave), self.color)
        screen.draw.filled_circle((self.x + 15, body_y + 8 - arm_wave), 3, self.color)
        
       
        eye_offset = 9
        eye_y = body_y - 5
        
        screen.draw.filled_circle((self.x - eye_offset, eye_y), 8, (255, 255, 255))
        screen.draw.filled_circle((self.x + eye_offset, eye_y), 8, (255, 255, 255))
        
    
        iris_color = (100, 255, 100) if self.enemy_type == "green" else (255, 100, 200)
        screen.draw.filled_circle((self.x - eye_offset, eye_y), 6, iris_color)
        screen.draw.filled_circle((self.x + eye_offset, eye_y), 6, iris_color)
        
    
        pupil_offset = 2 if frame_offset % 2 == 0 else -2
        screen.draw.filled_circle((self.x - eye_offset + pupil_offset, eye_y), 4, (0, 0, 0))
        screen.draw.filled_circle((self.x + eye_offset + pupil_offset, eye_y), 4, (0, 0, 0))
        
   
        screen.draw.filled_circle((self.x - eye_offset - 2, eye_y - 2), 2, (255, 255, 255))
        screen.draw.filled_circle((self.x + eye_offset - 2, eye_y - 2), 2, (255, 255, 255))
  
        mouth_y = body_y + 5
        screen.draw.line((self.x - 5, mouth_y), (self.x + 5, mouth_y), (50, 50, 50))
        
        
        antenna_wave = math.sin(self.animation_frame * 4) * 3
        antenna_color = (255, 255, 100) if self.enemy_type == "green" else (255, 100, 255)
       
        screen.draw.line((self.x - 10, body_y - 12), 
                        (self.x - 13, body_y - 22 + antenna_wave), self.color)
        screen.draw.filled_circle((self.x - 13, body_y - 22 + antenna_wave), 4, antenna_color)
        screen.draw.filled_circle((self.x - 13, body_y - 22 + antenna_wave), 2, (255, 255, 255))
        
        screen.draw.line((self.x + 10, body_y - 12), 
                        (self.x + 13, body_y - 22 - antenna_wave), self.color)
        screen.draw.filled_circle((self.x + 13, body_y - 22 - antenna_wave), 4, antenna_color)
        screen.draw.filled_circle((self.x + 13, body_y - 22 - antenna_wave), 2, (255, 255, 255))
        
        
        if self.enemy_type == "green":
            screen.draw.filled_circle((self.x - 5, body_y + 3), 2, (80, 200, 80))
            screen.draw.filled_circle((self.x + 4, body_y - 2), 2, (80, 200, 80))
        else:
            screen.draw.filled_circle((self.x - 5, body_y + 3), 2, (255, 120, 180))
            screen.draw.filled_circle((self.x + 4, body_y - 2), 2, (255, 120, 180))


class Game:
   
    
    def __init__(self):
        self.state = STATE_MENU
        self.level = 1
        self.player = None
        self.enemies = []
        self.obstacles = []
        self.portal = None
        self.sounds_enabled = True
        self.menu_selection = 0
        self.dt_accumulator = 0
        self.planet_intro_timer = 0
        
    def start_level(self):
      
        self.state = STATE_PLANET_INTRO
        self.planet_intro_timer = 0
        
      
        self.enemies.clear()
        self.obstacles.clear()
        
        
        self.player = Player(2, 2)
        
        
        num_obstacles = 8 + self.level * 2
        for _ in range(num_obstacles):
            while True:
                x = random.randint(1, GRID_WIDTH - 2)
                y = random.randint(1, GRID_HEIGHT - 2)
                if (x, y) != (2, 2) and (x, y) != (GRID_WIDTH - 3, GRID_HEIGHT - 3):
                    if not any(obs['x'] == x and obs['y'] == y for obs in self.obstacles):
                        self.obstacles.append({'x': x, 'y': y})
                        break
        
       
        num_enemies = 3 + self.level
        for i in range(num_enemies):
            while True:
                x = random.randint(3, GRID_WIDTH - 3)
                y = random.randint(3, GRID_HEIGHT - 3)
                if (abs(x - 2) + abs(y - 2)) > 4:  # Not too close to player
                    enemy_type = "green" if i % 2 == 0 else "pink"
                    self.enemies.append(Enemy(x, y, enemy_type))
                    break
        
      
        self.portal = {'x': GRID_WIDTH - 3, 'y': GRID_HEIGHT - 3}
        
    def check_collisions(self):
        """Check player-enemy collisions"""
        for enemy in self.enemies:
            if (self.player.grid_x == enemy.grid_x and 
                self.player.grid_y == enemy.grid_y):
                self.state = STATE_GAME_OVER
              
                try:
                    sounds.game_music.stop()
                except:
                    pass
                try:
                    if self.sounds_enabled:
                        sounds.over.play()
                except Exception as e:
                    pass
                return
                
    def check_portal(self):
        """Check if player reached portal"""
        if (self.player.grid_x == self.portal['x'] and 
            self.player.grid_y == self.portal['y']):
          
            self.level += 1
            self.start_level()



game = Game()



try:
    print("Attempting to load menu music...")

except Exception as e:
    print(f"Music init error: {e}")


def draw():
    """Main draw function"""
    if game.state == STATE_MENU:
        draw_menu()
    elif game.state == STATE_PLANET_INTRO:
        draw_planet_intro()
    elif game.state == STATE_PLAYING:
        draw_game()
    elif game.state == STATE_GAME_OVER:
        draw_game_over()
    elif game.state == STATE_LEVEL_COMPLETE:
        draw_level_complete()


def draw_planet_intro():
   
    screen.fill((10, 10, 30))
    
    
    for i in range(100):
        x = (i * 37 + game.level * 13) % WIDTH
        y = (i * 71) % HEIGHT
        size = 1 + (i % 3)
        twinkle = abs(math.sin(game.dt_accumulator * 2 + i * 0.5)) * 50 + 205
        screen.draw.filled_circle((x, y), size, (twinkle, twinkle, twinkle))
    
   
    planet_name = PLANET_NAMES[(game.level - 1) % len(PLANET_NAMES)]
    
    
    colors = [
        (255, 100, 255),  
        (255, 255, 100),  
        (200, 100, 255),  
    ]
    color_index = (game.level - 1) % len(colors)
    neon_color = colors[color_index]
    
   
    for offset in range(5, 0, -1):
        alpha_color = tuple(list(neon_color) + [50])
        screen.draw.text(f"LEVEL {game.level}", 
                        center=(WIDTH // 2, HEIGHT // 2 - 80 + offset), 
                        fontsize=35, color=alpha_color)
    
 
    screen.draw.text(f"LEVEL {game.level}", 
                    center=(WIDTH // 2, HEIGHT // 2 - 80), 
                    fontsize=35, color=neon_color)
    
 
    for offset in range(5, 0, -1):
        alpha_color = tuple(list(neon_color) + [50])
        screen.draw.text(planet_name, 
                        center=(WIDTH // 2, HEIGHT // 2), 
                        fontsize=50, color=alpha_color)
    
    screen.draw.text(planet_name, 
                    center=(WIDTH // 2, HEIGHT // 2), 
                    fontsize=50, color=neon_color)
    
   
    screen.draw.text("GET READY!", 
                    center=(WIDTH // 2, HEIGHT // 2 + 80), 
                    fontsize=35, color=(255, 255, 255))
    
    
    pulse = abs(math.sin(game.dt_accumulator * 3)) * 100 + 155
    screen.draw.text(f"Enemies: {len(game.enemies)}", 
                    center=(WIDTH // 2, HEIGHT // 2 + 130), 
                    fontsize=25, color=(pulse, pulse, 255))


def draw_menu():
    """Draw main menu"""
    
    screen.fill((10, 10, 30))
    for i in range(50):
        x = (i * 37) % WIDTH
        y = (i * 71) % HEIGHT
        brightness = 150 + (i * 13) % 100
        screen.draw.filled_circle((x, y), 1, (brightness, brightness, brightness))
    
   
    screen.draw.text("SPACE CAT", center=(WIDTH // 2, 100), 
                    fontsize=60, color=(255, 255, 100))
    screen.draw.text("ADVENTURE", center=(WIDTH // 2, 160), 
                    fontsize=40, color=(100, 255, 255))
    
   
    menu_items = ["START GAME", "MUSIC: ON" if game.sounds_enabled else "MUSIC: OFF", "EXIT"]
    for i, item in enumerate(menu_items):
        y = 280 + i * 60
        color = (255, 255, 0) if i == game.menu_selection else (200, 200, 200)
        prefix = "> " if i == game.menu_selection else "  "
        screen.draw.text(prefix + item, center=(WIDTH // 2, y), 
                        fontsize=40, color=color)
    

    
   
    screen.draw.text("Arrow keys to move and SPACE to select", 
                    center=(WIDTH // 2, 520), fontsize=25, color=(150, 150, 150))


def draw_game():
    """Draw game screen"""
   
    planet_colors = [
        (30, 20, 60),   
        (60, 30, 20),   
        (20, 60, 60),   
        (60, 60, 20),  
    ]
    bg_color = planet_colors[(game.level - 1) % len(planet_colors)]
    screen.fill(bg_color)
    
    
    for i in range(40):
        x = (i * 43 + game.level * 17) % WIDTH
        y = (i * 67) % HEIGHT
        screen.draw.filled_circle((x, y), 1, (255, 255, 255))
    
    
    for i in range(GRID_WIDTH + 1):
        x = i * CELL_SIZE
        screen.draw.line((x, 0), (x, HEIGHT), (255, 255, 255, 30))
    for i in range(GRID_HEIGHT + 1):
        y = i * CELL_SIZE
        screen.draw.line((0, y), (WIDTH, y), (255, 255, 255, 30))
    
    
    for obs in game.obstacles:
        x = obs['x'] * CELL_SIZE + CELL_SIZE // 2
        y = obs['y'] * CELL_SIZE + CELL_SIZE // 2
        screen.draw.filled_circle((x, y), 18, (80, 80, 80))
        screen.draw.filled_circle((x - 5, y - 5), 4, (100, 100, 100))
    
    
    portal_pulse = abs(math.sin(game.dt_accumulator * 3)) * 10
    portal_x = game.portal['x'] * CELL_SIZE + CELL_SIZE // 2
    portal_y = game.portal['y'] * CELL_SIZE + CELL_SIZE // 2
    screen.draw.filled_circle((portal_x, portal_y), 20 + portal_pulse, 
                             (100, 100, 255, 100))
    screen.draw.filled_circle((portal_x, portal_y), 15 + portal_pulse, 
                             (150, 150, 255, 150))
    screen.draw.text("EXIT", center=(portal_x, portal_y - 30), 
                    fontsize=20, color=(255, 255, 255))
    
    for enemy in game.enemies:
        enemy.draw()
    
    game.player.draw()
    
    screen.draw.text(f"LEVEL: {game.level}", topleft=(10, 10), 
                    fontsize=30, color=(255, 255, 255))
    screen.draw.text(f"ENEMIES: {len(game.enemies)}", topleft=(10, 45), 
                    fontsize=25, color=(255, 100, 100))
    
    
    sound_x = WIDTH - 70
    sound_y = 25
    button_width = 60
    button_height = 30
    button_color = (0, 200, 100) if game.sounds_enabled else (200, 100, 0)
    screen.draw.filled_rect(Rect(sound_x - button_width // 2, sound_y - button_height // 2, button_width, button_height), button_color)
    screen.draw.rect(Rect(sound_x - button_width // 2, sound_y - button_height // 2, button_width, button_height), (255, 255, 255))
    sound_text = "ON" if game.sounds_enabled else "OFF"
    screen.draw.text(sound_text, center=(sound_x, sound_y), fontsize=16, color=(255, 255, 255))
    
    screen.draw.text("WASD/ARROWS: Move | M: Mute", bottomleft=(10, HEIGHT - 10), 
                    fontsize=20, color=(200, 200, 200))


def draw_game_over():

    screen.fill((0, 0, 0))
    
    
    for i in range(100):
        x = (i * 37 + game.level * 13) % WIDTH
        y = (i * 71) % HEIGHT
        size = 1 + (i % 3)
        twinkle = abs(math.sin(game.dt_accumulator * 2 + i * 0.5)) * 50 + 205
        screen.draw.filled_circle((x, y), size, (twinkle, twinkle, twinkle))
    
 
    draw_game()
    
   
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0, 180))
    
   
    for offset in range(3, 0, -1):
        screen.draw.text("GAME OVER!", center=(WIDTH // 2, HEIGHT // 2 - 50 + offset), 
                        fontsize=70, color=(255, 50, 50, 100))
    
   
    screen.draw.text("GAME OVER!", center=(WIDTH // 2, HEIGHT // 2 - 50), 
                    fontsize=70, color=(255, 50, 50))
    
    
    screen.draw.text(f"Level Reached: {game.level}", 
                    center=(WIDTH // 2, HEIGHT // 2 + 20), 
                    fontsize=35, color=(255, 200, 100))
    
   
    pulse = abs(math.sin(game.dt_accumulator * 3)) * 30 + 200
    enemies_defeated = (game.level - 1) * 5
    screen.draw.text(f"Enemies Defeated: {enemies_defeated}", 
                    center=(WIDTH // 2, HEIGHT // 2 + 60), 
                    fontsize=30, color=(pulse, 255, pulse))
    
 
    screen.draw.text("Press SPACE to return to menu", 
                    center=(WIDTH // 2, HEIGHT // 2 + 120), 
                    fontsize=25, color=(200, 200, 200))


def draw_level_complete():
    """Draw level complete screen"""
    draw_game()
    
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 50, 180))
    
    screen.draw.text("LEVEL COMPLETE!", center=(WIDTH // 2, HEIGHT // 2 - 50), 
                    fontsize=60, color=(100, 255, 100), 
                    shadow=(2, 2), scolor=(0, 100, 0))
    screen.draw.text(f"Next: Planet {game.level}", 
                    center=(WIDTH // 2, HEIGHT // 2 + 30), 
                    fontsize=35, color=(255, 255, 255))
    screen.draw.text("Press SPACE to continue", 
                    center=(WIDTH // 2, HEIGHT // 2 + 80), 
                    fontsize=25, color=(200, 200, 200))


def update(dt):
    """Main update function"""
    game.dt_accumulator += dt
    
    if game.state == STATE_PLANET_INTRO:
        game.planet_intro_timer += dt
        if game.planet_intro_timer >= 3.0:  
            game.state = STATE_PLAYING
            
            try:
                if game.sounds_enabled:
                    sounds.game_music.play()
            except Exception as e:
                pass
    
    elif game.state == STATE_PLAYING:
     
        game.player.update_position(dt)
        game.player.update_animation(dt)
        
        
        for enemy in game.enemies:
            enemy.update(dt, game.obstacles, game.player, game.enemies)
        
        
        game.check_collisions()
        game.check_portal()


def on_mouse_down(pos):

    sound_x = WIDTH - 70
    sound_y = 25
    button_width = 60
    button_height = 30
    
    if (sound_x - button_width // 2 <= pos[0] <= sound_x + button_width // 2 and
        sound_y - button_height // 2 <= pos[1] <= sound_y + button_height // 2):
        game.sounds_enabled = not game.sounds_enabled
      
        if not game.sounds_enabled:
            try:
                sounds.game_music.stop()
            except:
                pass
     
        else:
            try:
                sounds.game_music.play(-1) 
            except:
                pass
        return
    
    if game.state == STATE_PLAYING:
        pass


def on_key_down(key):
  
    if game.state == STATE_MENU:
        if key in (keys.UP, keys.W):
            game.menu_selection = (game.menu_selection - 1) % 3
        elif key in (keys.DOWN, keys.S):
            game.menu_selection = (game.menu_selection + 1) % 3
        elif key == keys.SPACE:
            if game.menu_selection == 0:  
                game.level = 1
                game.start_level()
                try:
                    sounds.game_music.stop()
                except:
                    pass
            elif game.menu_selection == 1:  
                game.sounds_enabled = not game.sounds_enabled
                if not game.sounds_enabled:
                    try:
                        sounds.game_music.stop()
                    except:
                        pass
                else:
                    try:
                        sounds.game_music.play(-1)
                    except Exception as e:
                        pass
            elif game.menu_selection == 2:  
                exit()
    
    elif game.state == STATE_PLANET_INTRO:
        if key == keys.SPACE:
            game.state = STATE_PLAYING
            try:
                if game.sounds_enabled:
                    sounds.game_music.play()
            except Exception as e:
                pass
                
    elif game.state == STATE_PLAYING:
        if key in (keys.UP, keys.W):
            game.player.move(0, -1, game.obstacles, game.enemies)
        elif key in (keys.DOWN, keys.S):
            game.player.move(0, 1, game.obstacles, game.enemies)
        elif key in (keys.LEFT, keys.A):
            game.player.move(-1, 0, game.obstacles, game.enemies)
        elif key in (keys.RIGHT, keys.D):
            game.player.move(1, 0, game.obstacles, game.enemies)
        elif key == keys.M:  
            game.sounds_enabled = not game.sounds_enabled
            if not game.sounds_enabled:
                try:
                    sounds.game_music.stop()
                except:
                    pass
            else:
                try:
                    sounds.game_music.play(-1)
                except:
                    pass
            
    elif game.state == STATE_GAME_OVER:
        if key == keys.SPACE:
            game.state = STATE_MENU
            game.menu_selection = 0
            try:
                sounds.over.stop()
                if game.sounds_enabled:
                    sounds.game_music.play(-1)
            except Exception as e:
                pass
            
    elif game.state == STATE_LEVEL_COMPLETE:
        if key == keys.SPACE:
            game.start_level()



pgzrun.go()
