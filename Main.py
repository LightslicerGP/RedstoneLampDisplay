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
        - Pixels per lamp,
        - Lamps per pixel (2 is default)
        """
        self.size = (width, height)
        self.lampTextureSize = lampTextureSize

        if origin.upper() in ["TL", "BL"]:
            self.origin = origin.upper()
        else:
            print("origin is not either 'TL' or 'BL'")
            exit()

        self.lampsPerPixel = lampsPerPixel
        self.scale = scale
        self.displayState = [[False for _ in range(height)] for _ in range(width)]
        self.textureLocation = texturePack

        pygame.display.set_mode(
            (
                width * lampTextureSize * lampsPerPixel * scale,
                height * lampTextureSize * lampsPerPixel * scale,
            )
        )

        redstone_lamp_off = pygame.transform.scale(
            pygame.image.load(self.textureLocation + "/redstone_lamp.png"),
            (self.lampTextureSize * self.scale, self.lampTextureSize * self.scale),
        )

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                screen = pygame.display.get_surface()
                for x_width in range(self.lampsPerPixel):
                    for y_width in range(self.lampsPerPixel):
                        screen.blit(
                            redstone_lamp_off,
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
                    timestamp = datetime.datetime.now().strftime(
                        "%Y_%m_%d.%H_%M_%S.%f"
                    )[
                        :-3
                    ]  # Including milliseconds
                    directory = "screenshots/"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
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
        redstone_lamp_off = pygame.transform.scale(
            pygame.image.load(self.textureLocation + "/redstone_lamp.png"),
            (self.lampTextureSize * self.scale, self.lampTextureSize * self.scale),
        )
        redstone_lamp_on = pygame.transform.scale(
            pygame.image.load(self.textureLocation + "/redstone_lamp_on.png"),
            (self.lampTextureSize * self.scale, self.lampTextureSize * self.scale),
        )

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                y_adjusted = self.size[1] - y - 1 if self.origin == "BL" else y
                screen = pygame.display.get_surface()

                for x_width in range(self.lampsPerPixel):
                    for y_width in range(self.lampsPerPixel):
                        screen.blit(
                            (
                                redstone_lamp_off
                                if self.displayState[x][y] == False
                                else redstone_lamp_on
                            ),
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

width = 20
height = 20

display = Display(width, height, scale=1.5, texturePack="MattPack")

while display.alive():

    display.set(random.randint(0, width - 1), random.randint(0, height - 1), True)
    display.set(random.randint(0, width - 1), random.randint(0, height - 1), False)

    display.push_buffer()
