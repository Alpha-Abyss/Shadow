import pygame
import sys
import os
from Levels import JSONMapLoader

pygame.init()

#----- Screen
get_screen = pygame.display.Info()
sw, sh = get_screen.current_w, get_screen.current_h
size = sw / 2, sh / 2
Screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Shadow")

#----- Player
class PLAYER(pygame.sprite.Sprite):
    def __init__(self, base_path=None):
        super().__init__()
        # Set base_path to the directory containing the spritesheets
        if base_path is None:
            base_path = os.path.join(os.path.dirname(__file__), 'Assets', 'Player')
        
        self.sprit_type = {
            "idle": (os.path.join(base_path, "Idel.png"), 10, (48, 48)),
            "run": (os.path.join(base_path, "Run.png"), 8, (48, 48)),
            "jump": (os.path.join(base_path, "Jump.png"), 6, (48, 48)),
            "climb": (os.path.join(base_path, "LedgeClimb64x64.png"), 11, (64, 64)),
            "push": (os.path.join(base_path, "Push.png"), 6, (48, 48)),
            "wallslide": (os.path.join(base_path, "Wall-slid.png"), 8, (48, 48))
        }
        self.sprites = self.load_spritesheets()
        self.current_action = "idle"
        self.current_frame = 0
        self.image = self.sprites[self.current_action][self.current_frame]
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.speed = 200  # pixels per second
        self.gravity = 1000  # pixels per second squared
        self.jump_speed = -500  # pixels per second (upward)
        self.velocity_y = 0
        self.on_ground = False
        self.animation_timer = 0
        self.facing_right = True  # Track the direction the player is facing

    def load_spritesheets(self):
        sprites = {}
        for action, (filename, frame_count, size) in self.sprit_type.items():
            sheet = pygame.image.load(filename).convert_alpha()
            sprites[action] = self.cut_sprites(sheet, frame_count, size)
        return sprites

    @staticmethod
    def cut_sprites(sheet, frame_count, size):
        sprite_width, sprite_height = size
        return [sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height)) for i in range(frame_count)]

    def update(self, dt):
        self.handle_input(dt)
        self.apply_gravity(dt)
        self.animate(dt)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        self.on_ground = self.rect.bottom >= 400  # Example ground level

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
            self.facing_right = False  # Player is facing left
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
            self.facing_right = True  # Player is facing right

        # Prioritize jump animation when not on the ground
        if not self.on_ground:
            self.current_action = "jump"
        else:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.current_action = "run"
            else:
                self.current_action = "idle"

        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False  # Player is no longer on the ground
            self.current_action = "jump"

    def apply_gravity(self, dt):
        # Apply gravity and update the player's vertical position
        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y * dt
        
        # Check if the player has landed on the ground
        if self.rect.bottom >= 400:  # Example ground level
            self.rect.bottom = 400
            self.velocity_y = 0
            self.on_ground = True
            if not (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]):
                self.current_action = "idle"  # Reset to idle if no movement keys are pressed

    def animate(self, dt):
        self.animation_timer += dt
        animation_speed = 0.1  # Adjust this for global animation speed control
        if self.animation_timer > animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_action])
            self.image = self.sprites[self.current_action][self.current_frame]
            
            # Flip the image based on the direction
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

#----- MAIN
def gameloop():
    clock = pygame.time.Clock()

    # Load the JSON map
    map_loader = JSONMapLoader("Shadow\SHADOW\Assets\Levels\L1.json")
    
    # Create player instance and sprite group
    player = PLAYER()
    all_sprites = pygame.sprite.Group(player)

    # Initialize camera
    camera_x, camera_y = 0, 0

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        Screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Handle player movement and update camera position
        player.update(dt)
        
        # Update camera position based on player's position
        camera_x = player.rect.centerx - size[0] // 2
        camera_y = player.rect.centery - size[1] // 2
        
        # Draw the map with scrolling effect
        map_loader.draw(Screen, camera_x, camera_y)

        # Draw all sprites
        all_sprites.draw(Screen) 
        
        pygame.display.update()

if __name__ == '__main__':
    gameloop()