import pygame
import sys

pygame.init()

#----- Screen
get_screen = pygame.display.Info()
sw, sh = get_screen.current_w, get_screen.current_h
size = sw / 2, sh / 2
Screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Shadow")

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