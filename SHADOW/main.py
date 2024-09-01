import pygame
import sys

pygame.init()

#----- Screen
get_screen = pygame.display.Info()
sw, sh = get_screen.current_w, get_screen.current_h
size = sw / 2, sh / 2
Screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Shadow")

#----- Player
class PLAYER(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprit_type = {"idle": "Idle.png",
                           "run": "Run.png",
                           "jump": "Jump.png",
                           "climb": "LedgeClimb64x64.png",
                           "push": "Push.png",
                           "wall-slid": "Wall-slid.png"}
        self.load_sprite_sheet()
        self.current_frame = 0
        self.animation_frames = []
        self.load_frames()
    
    def load_sprite_sheet(self):
        self.image = pygame.
        

#----- MAIN
def gameloop():
    running = True
    while running:

        Screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

if __name__ == '__main__':
    Game = gameloop()
    Game