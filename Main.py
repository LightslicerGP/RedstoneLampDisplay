import pygame
import os
import datetime


class Display:
    def __init__(
        self,
        width: int,
        height: int,
        lampTextureSize: int = 16,
        origin: str = "BL",
        lampsPerPixel: int = 2,
        scale: int = 1,
        texturePack: str = "VanillaPack",
    ):
        """
        Initialize the display with:
        - Width and Height of the display (Lamp count),
        - Texture size of the lamp (default is 16),
        - Origin on the y axis (default is bottom left, "BL")
        - Lamps per pixel (default is 2)
        - Scale (default is 1x)
        - Texture pack (default is VanillaPack)
        """
        self.size = (width, height)
        self.lampTextureSize = lampTextureSize

        if origin.upper() not in ["TL", "BL"]:
            print("origin is not either 'TL' or 'BL'")
            exit()
        self.origin = origin.upper()

        self.lampsPerPixel = lampsPerPixel
        self.scale = scale
        self.displayState = [[False] * height for _ in range(width)]
        self.textureLocation = texturePack

        pygame.display.set_mode(
            (
                width * lampTextureSize * lampsPerPixel * scale,
                height * lampTextureSize * lampsPerPixel * scale,
            )
        )

        self.redstone_lamp_on = pygame.transform.scale(
            pygame.image.load(self.textureLocation + "/redstone_lamp_on.png"),
            (self.lampTextureSize * self.scale, self.lampTextureSize * self.scale),
        )
        self.redstone_lamp_off = pygame.transform.scale(
            pygame.image.load(self.textureLocation + "/redstone_lamp.png"),
            (self.lampTextureSize * self.scale, self.lampTextureSize * self.scale),
        )

        screen = pygame.display.get_surface()
        
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                
                for x_width in range(self.lampsPerPixel):
                    for y_width in range(self.lampsPerPixel):
                        
                        screen.blit(
                            self.redstone_lamp_off,
                            (
                                (
                                    (x * self.lampTextureSize * self.lampsPerPixel)
                                    + (x_width * self.lampTextureSize)
                                )
                                * self.scale,
                                (
                                    (y * self.lampTextureSize * self.lampsPerPixel)
                                    + (y_width * self.lampTextureSize)
                                )
                                * self.scale,
                            ),
                        )

    def alive(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_s:
                    timestamp = datetime.datetime.now().strftime("%Y_%m_%d.%H_%M_%S.%f")[:-3]
                    directory = "screenshots/"
                    os.makedirs(directory, exist_ok=True)
                    filename = f"{directory}screenshot_{timestamp}.png"
                    pygame.image.save(pygame.display.get_surface(), filename)
                    print("Screenshot saved as:", filename)
        return True

    def set(self, x, y, state):
        self.displayState[x][y] = state

    def clear(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.displayState[x][y] = False

    def push_buffer(self):

        screen = pygame.display.get_surface()
        
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                
                y_adjusted = self.size[1] - y - 1 if self.origin == "BL" else y
                
                for x_width in range(self.lampsPerPixel):
                    for y_width in range(self.lampsPerPixel):
                        
                        screen.blit(
                            self.redstone_lamp_on if self.displayState[x][y] else self.redstone_lamp_off,
                            (
                                (
                                    (x * self.lampTextureSize * self.lampsPerPixel)
                                    + (x_width * self.lampTextureSize)
                                )
                                * self.scale,
                                (
                                    (y_adjusted * self.lampTextureSize * self.lampsPerPixel)
                                    + (y_width * self.lampTextureSize)
                                )
                                * self.scale,
                            ),
                        )
                        
        pygame.display.update()


import random

width = 100
height = 100

display = Display(width, height, scale=0.5, lampsPerPixel=1, texturePack="B&WPack")

while display.alive():

    display.set(random.randint(0, width - 1), random.randint(0, height - 1), True)
    display.set(random.randint(0, width - 1), random.randint(0, height - 1), False)

    display.push_buffer()
