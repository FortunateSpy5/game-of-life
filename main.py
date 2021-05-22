import pygame
import numpy as np
from time import sleep

class GameOfLife:
    def __init__(self):
        pygame.init()
        self.size = 800
        self.divisions = 100
        self.length = self.size // self.divisions
        self.screen = pygame.display.set_mode((self.size, self.size))
        self.fps = 120
        self.interval = 10
        self.counter = 0
        self.color_bg = (25, 25, 25)
        self.color_fg = (230, 230, 230)
        self.cells = np.full((self.divisions, self.divisions), False, dtype=bool)
        self.paused = False

    def play(self):
        clock = pygame.time.Clock()

        self.draw()
        pygame.display.update()

        while True:
            self.counter += 1
            clock.tick(self.fps)
            self.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.paused = not self.paused
                self.draw()
                pygame.display.update()
                sleep(0.2)
            
            if self.paused:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    pos = [pos[0] // self.length, pos[1] // self.length]
                    self.cells[pos[0], pos[1]] = not self.cells[pos[0], pos[1]]
                continue

            if self.counter % (self.fps // self.interval) == 0:
                neighbors_count = np.full((self.divisions + 2, self.divisions + 2), 0, dtype=np.int8)
                
                for i in range(self.divisions):
                    for j in range(self.divisions):
                        if self.cells[i, j]:
                            for i2 in range(i, i+3):
                                for j2 in range(j, j+3):
                                    neighbors_count[i2, j2] += 1
                            neighbors_count[i+1, j+1] -= 1
                
                for i in range(self.divisions):
                    for j in range(self.divisions):
                        if self.cells[i, j]:
                            if neighbors_count[i+1, j+1] not in {2, 3}:
                                self.cells[i, j] = False
                        else:
                            if neighbors_count[i+1, j+1] == 3:
                                self.cells[i, j] = True
    
    def draw(self):
        pygame.draw.rect(
            self.screen, 
            self.color_bg,
            pygame.Rect(0, 0, self.size, self.size)
        )
        for i in range(self.divisions):
            for j in range(self.divisions):
                if self.cells[i, j]:
                    pygame.draw.rect(
                        self.screen, 
                        self.color_fg, 
                        pygame.Rect(i * self.length, j * self.length, self.length, self.length)
                    )

if __name__ == "__main__":
    obj = GameOfLife()
    obj.play()