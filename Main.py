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
        self.lampsPerPixel = lampsPerPixel
        if origin.upper() not in ["TL", "BL"]:
            print("origin is not either 'TL' or 'BL'")
            exit()
        self.origin = origin.upper()

        self.scale = scale
        self.displayState = [[False] * height for _ in range(width)]
        self.textureLocation = texturePack
        self.changed_cells = set()
        self.dirty_rects = []

        self.lamp_pixel_size = lampTextureSize * scale
        self.pixel_size = self.lamp_pixel_size * lampsPerPixel

        self.screen = pygame.display.set_mode(
            (
                width * self.pixel_size,
                height * self.pixel_size,
            ),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        texture_size_scaled = (self.lamp_pixel_size, self.lamp_pixel_size)
        self.redstone_lamp_on = pygame.transform.scale(
            pygame.image.load(os.path.join(self.textureLocation, "redstone_lamp_on.png")),
            texture_size_scaled,
        ).convert()
        self.redstone_lamp_off = pygame.transform.scale(
            pygame.image.load(os.path.join(self.textureLocation, "redstone_lamp.png")),
            texture_size_scaled,
        ).convert()


        for x in range(self.size[0]):
            for y in range(self.size[1]):
                y_adjusted = self.size[1] - y - 1 if self.origin == "BL" else y
                texture = self.redstone_lamp_off
                base_pos_x = x * self.pixel_size
                base_pos_y = y_adjusted * self.pixel_size

                for x_width in range(self.lampsPerPixel):
                    for y_width in range(self.lampsPerPixel):
                        pos_x = base_pos_x + (x_width * self.lamp_pixel_size)
                        pos_y = base_pos_y + (y_width * self.lamp_pixel_size)
                        rect = pygame.Rect(pos_x, pos_y, self.lamp_pixel_size, self.lamp_pixel_size)
                        self.screen.blit(texture, rect)

        pygame.display.flip()



    def alive(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_s:
                    self.screenshot()
        return True

    def screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d.%H_%M_%S.%f")[:-3]
        directory = "screenshots/"
        os.makedirs(directory, exist_ok=True)
        filename = f"{directory}screenshot_{timestamp}.png"
        pygame.image.save(pygame.display.get_surface(), filename)
        print("Screenshot saved as:", filename)

    def set(self, x, y, state):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and self.displayState[x][y] != state:
            self.displayState[x][y] = state
            self.changed_cells.add((x, y))


    def clear(self):
        updated = False
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.displayState[x][y]:
                    self.displayState[x][y] = False
                    self.changed_cells.add((x, y))
                    updated = True
        return updated


    def push_buffer(self):
        if not self.changed_cells:
            return

        self.dirty_rects = []

        for x, y in self.changed_cells:
            y_adjusted = self.size[1] - y - 1 if self.origin == "BL" else y
            texture = self.redstone_lamp_on if self.displayState[x][y] else self.redstone_lamp_off
            base_pos_x = x * self.pixel_size
            base_pos_y = y_adjusted * self.pixel_size
            rects_to_update = []

            for x_width in range(self.lampsPerPixel):
                for y_width in range(self.lampsPerPixel):
                    pos_x = base_pos_x + (x_width * self.lamp_pixel_size)
                    pos_y = base_pos_y + (y_width * self.lamp_pixel_size)
                    rect = pygame.Rect(pos_x, pos_y, self.lamp_pixel_size, self.lamp_pixel_size)
                    self.screen.blit(texture, rect)
                    rects_to_update.append(rect)

            self.dirty_rects.extend(rects_to_update)

        self.changed_cells.clear()
        pygame.display.update(self.dirty_rects)
        self.dirty_rects = []

width = 640
height = 480

display = Display(width, height, scale=0.125, lampsPerPixel=1, texturePack="MinimalPack")

ball_x = 1
ball_y = 0

ball_velocity_x = 1
ball_velocity_y = 1

while display.alive():

    display.clear()

    # Ball position and velocity
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Check for collision with walls
    if ball_x >= width - 1 or ball_x <= 0:
        ball_velocity_x *= -1
    if ball_y >= height - 1 or ball_y <= 0:
        ball_velocity_y *= -1

    # Set the ball position on the display
    display.set(ball_x, ball_y, True)

    display.push_buffer()
