from random import randint
import pygame as pg
from pygame import gfxdraw
SW, SH = 1280, 720

art_styles_list = [
    "Chaotic",
    "Striped Horizontal",
    "Striped Vertical",
    "Mosaic",
    "Cornered",
    "Centered",
    "Empty"
]

art_shapes_list = [
    "Lines",
    "Circles",
    "Squares",
    "Hollow Polygons",
    "Filled Polygons",
    "Dots",
    "Curves",
    "Rings"
]

class Canvas:
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        self.canvas = pg.Surface((self.width, self.height))
        self.canvas.fill((255, 255, 255))

        self.bg_layer = pg.Surface((self.width, self.height))
        self.bg_layer.fill((255, 255, 255))
        self.layer_one = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.layer_two = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.fg_layer = pg.Surface((self.width, self.height), pg.SRCALPHA)

    def clean_all_layers(self):
        self.layer_one.fill((0, 0, 0, 0))
        self.layer_two.fill((0, 0, 0, 0))

    def clean_layer(self, layer):
        layer.fill((0, 0, 0, 0))

    def generate_lines(self, complexity, cp, style, layer, magnitude):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity):
                posX = (randint(-200, self.width+200), randint(0, self.width))
                posY = (randint(-200, self.height+200), randint(0, self.height))
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1])
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size//4)
        elif style == art_styles_list[1]:   # Striped Horizontal
            interval = self.height // complexity
            for i in range(complexity):
                posX = 0, self.width
                posY = i * interval + randint(0, self.height//10), i * interval + randint(0, self.height//10)
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1])
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size // 4)
        elif style == art_styles_list[2]:   # Striped Vertical
            interval = self.width // complexity
            for i in range(complexity):
                posY = 0, self.height
                posX = i * interval + randint(0, self.width//10), i * interval + randint(0, self.width//10)
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1])
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size // 4)
        elif style == art_styles_list[3]:   # Mosaic
            row_line_count = complexity // 3 + 1
            row_count = complexity // 4 + 1
            x_interval = self.width // (row_line_count - 1)
            y_interval = self.height // (row_count - 1)
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_line_count):
                    current_color = color_one if (i+j) % 2 == 0 else color_two
                    size = randint(magnitude[0], magnitude[1]) // 4
                    posX = ((x_interval*j), (x_interval*(j+1)))
                    posY_u = ((y_interval*i), (y_interval*(i+1)))
                    posY_d = ((y_interval*(i+1)), (y_interval*i))
                    if randint(0,1) == 0:
                        pg.draw.line(layer, pg.Color(current_color), (posX[0], posY_u[0]), (posX[1], posY_u[1]), size)
                    else:
                        pg.draw.line(layer, pg.Color(current_color), (posX[0], posY_d[0]), (posX[1], posY_d[1]), size)

        elif style == art_styles_list[4]:   # Cornered
            for i in range(complexity*2):
                current_color = cp[randint(0, len(cp) - 1)]
                size = randint(magnitude[0], magnitude[1]) // 4
                corner = randint(0, 3)
                first_x_area, second_x_area = 0, 0
                first_y_area, second_y_area = 0, 0
                if corner == 0:
                    first_x_area, second_x_area = (-50, 100), (0, self.width//2)
                    first_y_area, second_y_area = (-50, 100), (0, self.height//2)
                elif corner == 1:
                    first_x_area, second_x_area = (self.width-100, self.width+50), (self.width//2, self.width)
                    first_y_area, second_y_area = (-50, 100), (0, self.height // 2)
                elif corner == 2:
                    first_x_area, second_x_area = (self.width-100, self.width+50), (self.width//2, self.width)
                    first_y_area, second_y_area = (self.height-100, self.height+50), (self.height//2, self.height)
                elif corner == 3:
                    first_x_area, second_x_area = (-50, 100), (0, self.width // 2)
                    first_y_area, second_y_area = (self.height-100, self.height+50), (self.height//2, self.height)

                posX = (randint(first_x_area[0], first_x_area[1]), randint(second_x_area[0], second_x_area[1]))
                posY = (randint(first_y_area[0], first_y_area[1]), randint(second_y_area[0], second_y_area[1]))

                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size)
        elif style == art_styles_list[5]:   # Centered
            for i in range(complexity//2):
                current_color = cp[randint(0, len(cp)-1)]
                posX = (randint(2*self.width//5, 3*self.width//5), randint(0, self.width))
                posY = (randint(2*self.height//5, 3*self.height//5), randint(0, self.height))
                size = randint(magnitude[0], magnitude[1]) // 4
                pg.draw.line(layer, pg.Color(current_color), (posX[0], posY[0]), (posX[1], posY[1]), size)
        elif style == art_styles_list[6]:   # Empty, do not draw anything.
            pass

    def generate_squares(self, complexity, cp, style, layer, magnitude):

        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity*2):
                size = randint(magnitude[0], magnitude[1])
                posX = randint(-size, self.width)
                posY = randint(-size, self.height)
                current_color = cp[randint(0, len(cp)-1)]
                pg.draw.rect(layer, pg.Color(current_color), (posX, posY, size, size))

        if style == art_styles_list[1]:     # Striped Horizontal
            row_square_count = complexity // 2 + 2
            point = self.width // (row_square_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                if i % 2 == 0:
                    current_color = color_one if current_color == color_two else color_two
                for j in range(row_square_count):
                    posX = j * point
                    posY = i * point
                    size = randint(magnitude[0], magnitude[1])
                    if i % 2 == 0:
                        pg.draw.rect(layer, pg.Color(current_color),(posX, posY, size, size))

        if style == art_styles_list[2]:     # Striped Vertical
            row_square_count = complexity // 2 + 2
            point = self.width // (row_square_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                for j in range(row_square_count):
                    if j % 1 == 0:
                        current_color = color_one if current_color == color_two else color_two
                    posX = j * point
                    posY = i * point
                    size = randint(magnitude[0], magnitude[1])
                    if j % 2 == 0:
                        pg.draw.rect(layer, pg.Color(current_color), (posX-size//2, posY-size//2, size, size))

        if style == art_styles_list[3]:     # Mosaic
            row_square_count = complexity//2 + 2
            size = self.width // (row_square_count-2)
            row_count = self.height // size + 2
            color_one = cp[randint(0, len(cp)-1)]
            color_two = cp[randint(0, len(cp)-1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                for j in range(row_square_count):
                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    posX = j * size
                    posY = i * size
                    pg.draw.rect(layer, pg.Color(current_color), (posX+size//20, posY+size//20, size-size//10, size-size//10))

        if style == art_styles_list[4]:     # Cornered
            for corner in range(4):
                corner_color = cp[randint(0, len(cp)-1)]
                if corner == 0:
                    pg.draw.rect(layer, pg.Color(corner_color), (0, 0, magnitude[1], magnitude[1]))
                if corner == 1:
                    pg.draw.rect(layer, pg.Color(corner_color), (self.width-magnitude[1], 0, magnitude[1], magnitude[1]))
                if corner == 2:
                    pg.draw.rect(layer, pg.Color(corner_color), (self.width-magnitude[1], self.height-magnitude[1], magnitude[1], magnitude[1]))
                if corner == 3:
                    pg.draw.rect(layer, pg.Color(corner_color), (0, self.height-magnitude[1], magnitude[1], magnitude[1]))

            for i in range(complexity*3):
                current_color = cp[randint(0, len(cp)-1)]
                corner = randint(0, 3)
                x_area, y_area = (0, 0), (0, 0)
                if corner == 0:
                    x_area, y_area = (-magnitude[1]//2, self.width//3), (-magnitude[1]//2, self.height//2-magnitude[1])
                if corner == 1:
                    x_area, y_area = (2*self.width//3-magnitude[1], self.width), (-magnitude[1]//2, self.height//2-magnitude[1])
                if corner == 2:
                    x_area, y_area = (2*self.width//3-magnitude[1], self.width), (self.height//2, self.height)
                if corner == 3:
                    x_area, y_area = (-magnitude[1], self.width//3), (self.height//2, self.height)

                posX = randint(x_area[0], x_area[1])
                posY = randint(y_area[0], y_area[1])
                size = randint(magnitude[0], magnitude[1])

                pg.draw.rect(layer, pg.Color(current_color), (posX, posY, size, size))

        if style == art_styles_list[5]:     # Centered
            in_x_area, in_y_area = (self.width // 4, 3 * self.width // 4), (self.height // 4, 3 * self.height // 4)
            out_x_area, out_y_area = (self.width // 6, 5 * self.width // 6), (self.height // 6, 5 * self.height // 6)

            for i in range(complexity):
                random_number = randint(0, 5)
                if random_number < 4:
                    center_x = randint(in_x_area[0], in_x_area[1])
                    center_y = randint(in_y_area[0], in_y_area[1])
                else:
                    center_x = randint(out_x_area[0], out_x_area[1])
                    center_y = randint(out_y_area[0], out_y_area[1])

                size = randint(magnitude[0], magnitude[1])
                current_color = cp[randint(0, len(cp) - 1)]

                pg.draw.rect(layer, pg.Color(current_color), (center_x-size//2, center_y-size//2, size, size))
        if style == art_styles_list[6]:     # Empty
            pass

    def generate_circles(self, complexity, cp, style, layer, magnitude, fill):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity):
                rad = randint(magnitude[0], magnitude[1])
                if fill == 1:
                    fill_type = randint(5, rad//2)
                else:
                    fill_type = 0
                centerX = randint(-25, self.width + 25)
                centerY = randint(-25, self.height + 25)
                current_color = cp[randint(0, len(cp) - 1)]
                alpha_surface = pg.Surface((rad*2, rad*2))
                alpha_surface.fill((0, 0, 0))
                pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                alpha_surface.set_colorkey((0, 0, 0))
                alpha_surface.set_alpha(randint(150, 255))
                layer.blit(alpha_surface, (centerX-rad, centerY-rad))

        if style == art_styles_list[1]:     # Striped Horizontal
            row_circle_count = complexity // 2 + 2
            point = self.width // (row_circle_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                if i % 2 == 0:
                    current_color = color_one if current_color == color_two else color_two
                for j in range(row_circle_count):
                    posX = j * point
                    posY = i * point
                    rad = randint(magnitude[0], magnitude[1])
                    if fill == 1:
                        fill_type = randint(5, rad // 2)
                    else:
                        fill_type = 0
                    if i % 2 == 0:
                        alpha_surface = pg.Surface((rad * 2, rad * 2))
                        alpha_surface.fill((0, 0, 0))
                        pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                        alpha_surface.set_colorkey((0, 0, 0))
                        alpha_surface.set_alpha(randint(150, 255))
                        layer.blit(alpha_surface, (posX - rad, posY - rad))

        if style == art_styles_list[2]:  # Striped Vertical
            row_circle_count = complexity // 2 + 2
            point = self.width // (row_circle_count - 2)
            row_count = self.height // point + 2
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]

            for i in range(row_count):
                for j in range(row_circle_count):
                    if (j+1) % 2 == 0:
                        current_color = color_one if current_color == color_two else color_two
                    posX = j * point
                    posY = i * point
                    rad = randint(magnitude[0], magnitude[1])
                    if fill == 1:
                        fill_type = randint(5, rad // 2)
                    else:
                        fill_type = 0
                    if j % 2 == 0:
                        alpha_surface = pg.Surface((rad * 2, rad * 2))
                        alpha_surface.fill((0, 0, 0))
                        pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                        alpha_surface.set_colorkey((0, 0, 0))
                        alpha_surface.set_alpha(randint(150, 255))
                        layer.blit(alpha_surface, (posX - rad, posY - rad))

        if style == art_styles_list[3]:     # Mosaic
            row_circle_count = complexity
            rad = self.width // row_circle_count
            row_count = self.height // rad + 1
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_circle_count):
                    if fill == 1:
                        fill_type = rad//4
                    else:
                        fill_type = 0
                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    posX = rad + j * (rad+1) * 2
                    posY = rad + i * (rad+1) * 2
                    pg.draw.circle(layer, pg.Color(current_color), (posX, posY), rad, fill_type)

        if style == art_styles_list[4]:     # Cornered
            for i in range(complexity*2):
                current_color = cp[randint(0, len(cp)-1)]
                corner = randint(0, 3)
                x_area, y_area = (0, 0), (0, 0)
                if corner == 0:
                    x_area, y_area = (-50, self.width//3), (-50, self.height//3)
                if corner == 1:
                    x_area, y_area = (self.width//1.5, self.width+50), (-50, self.height//3)
                if corner == 2:
                    x_area, y_area = (self.width//1.5, self.width+50), (self.height//1.5, self.height+50)
                if corner == 3:
                    x_area, y_area = (-50, self.width//3), (self.height//1.5, self.height+50)

                posX = randint(int(x_area[0]), int(x_area[1]))
                posY = randint(int(y_area[0]), int(y_area[1]))
                rad = randint(magnitude[0], magnitude[1])

                if fill == 1:
                    fill_type = randint(5, rad//2)
                else:
                    fill_type = 0

                alpha_surface = pg.Surface((rad * 2, rad * 2))
                alpha_surface.fill((0, 0, 0))
                pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                alpha_surface.set_colorkey((0, 0, 0))
                alpha_surface.set_alpha(randint(150, 255))
                layer.blit(alpha_surface, (posX - rad, posY - rad))

        if style == art_styles_list[5]:     # Centered
            in_x_area, in_y_area = (self.width//4, 3*self.width//4), (self.height//4, 3*self.height//4)
            out_x_area, out_y_area = (self.width//6, 5*self.width//6), (self.height//6, 5*self.height//6)

            for i in range(complexity):
                if fill == 1:
                    fill_type = randint(magnitude[0], magnitude[1])
                else:
                    fill_type = 0
                random_number = randint(0, 5)
                if random_number < 4:
                    center_x = randint(in_x_area[0], in_x_area[1])
                    center_y = randint(in_y_area[0], in_y_area[1])
                else:
                    center_x = randint(out_x_area[0], out_x_area[1])
                    center_y = randint(out_y_area[0], out_y_area[1])

                rad = randint(magnitude[0], magnitude[1])
                current_color = cp[randint(0, len(cp)-1)]

                if fill == 1:
                    fill_type = randint(5, rad//2)
                else:
                    fill_type = 0

                alpha_surface = pg.Surface((rad * 2, rad * 2))
                alpha_surface.fill((0, 0, 0))
                pg.draw.circle(alpha_surface, pg.Color(current_color), (rad, rad), rad, fill_type)
                alpha_surface.set_colorkey((0, 0, 0))
                alpha_surface.set_alpha(randint(150, 255))
                layer.blit(alpha_surface, (center_x - rad, center_y - rad))

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_polygons(self, complexity, cp, style, layer, magnitude, fill):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity//2):
                current_color = cp[randint(0, len(cp)-1)]
                if fill == 0:
                    fill_type = 0
                else:
                    fill_type = randint(magnitude[0]//5, magnitude[1]//5)
                points_count = randint(3, 5)
                points = []
                first_point = [randint(0, self.width), randint(0, self.height)]
                for _ in range(points_count):
                    points.append([randint(first_point[0]-magnitude[1]*2, first_point[0]+magnitude[1]*2),
                                   randint(first_point[1]-magnitude[1]*2, first_point[1]+magnitude[1]*2)])

                pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[1]:     # Striped Horizontal
            row_polygon_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_polygon_count
            y_interval = self.height // row_count

            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            for i in range(row_count):
                if (i + 1) % 2 == 0:
                    current_color = color_one if current_color == color_two else color_two
                for j in range(row_polygon_count):
                    if fill == 0:
                        fill_type = 0
                    else:
                        fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                    x_area = (x_interval * j, x_interval * (j + 1))
                    y_area = (y_interval * i, y_interval * (i + 1))
                    point_count = randint(3, 5)
                    points = []
                    if (i + 1) % 2 == 0:
                        for k in range(point_count):
                            points.append((randint(x_area[0], x_area[1]), randint(y_area[0], y_area[1])))
                        pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[2]:     # Striped Vertical
            row_polygon_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_polygon_count
            y_interval = self.height // row_count

            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            current_color = color_one
            for i in range(row_count):
                for j in range(row_polygon_count):
                    if fill == 0:
                        fill_type = 0
                    else:
                        fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                    x_area = (x_interval * j, x_interval * (j + 1))
                    y_area = (y_interval * i, y_interval * (i + 1))
                    point_count = randint(3, 5)
                    points = []
                    if j % 2 == 0:
                        current_color = color_one if current_color == color_two else color_two
                        for k in range(point_count):
                            points.append((randint(x_area[0], x_area[1]), randint(y_area[0], y_area[1])))
                        pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[3]:     # Mosaic
            row_polygon_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_polygon_count
            y_interval = self.height // row_count

            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_polygon_count):
                    if fill == 0:
                        fill_type = 0
                    else:
                        fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    x_area = (x_interval*j, x_interval*(j+1))
                    y_area = (y_interval*i, y_interval*(i+1))
                    point_count = randint(3, 5)
                    points = []
                    for k in range(point_count):
                        points.append((randint(x_area[0], x_area[1]), randint(y_area[0], y_area[1])))
                    pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[4]:     # Cornered
            x_areas = [(-100, self.width//3), (2*self.width//3, self.width+100),
                       (2*self.width//3, self.width+100), (-100, self.width//3)]

            y_areas = [(-100, self.height//2-50), (-100, self.height//2-100),
                       (self.height//2+100, self.height+100), (self.height//2+100, self.height+100)]

            point_count = randint(3, 5)
            for i in range(complexity//2):
                corner = randint(0, 3)
                if fill == 0:
                    fill_type = 0
                else:
                    fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)
                current_color = cp[randint(0, len(cp)-1)]
                points = []
                for j in range(point_count):
                    pos = (randint(x_areas[corner][0], x_areas[corner][1]),
                           randint(y_areas[corner][0], y_areas[corner][1]))
                    points.append(pos)

                pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[5]:     # Centered
            x_inner_area = [self.width // 4, 3 * self.width // 4]
            x_outer_area = [self.width // 6, 5 * self.width // 6]
            y_area = [self.height // 4, 3 * self.height // 4]
            for i in range(complexity // 4):
                if fill == 0:
                    fill_type = 0
                else:
                    fill_type = randint(magnitude[0] // 10, magnitude[1] // 10)

                current_color = cp[randint(0, len(cp)-1)]

                point_count = randint(3, 4)
                points = []
                for j in range(point_count):
                    if randint(0, 6) <= 4:
                        pos = (randint(x_inner_area[0], x_inner_area[1]), randint(y_area[0], y_area[1]))
                    else:
                        pos = (randint(x_outer_area[0], x_outer_area[1]), randint(y_area[0], y_area[1]))

                    points.append(pos)
                pg.draw.polygon(layer, pg.Color(current_color), points, fill_type)

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_curves(self, complexity, cp, style, layer, magnitude):
        if style == art_styles_list[0]:
            multiples = magnitude // 5
            for i in range(complexity//5):
                current_color = cp[randint(0, len(cp)-1)]
                point_count = 5
                multiples_points = []
                for _ in range(multiples):
                    multiples_points.append([])
                for j in range(point_count):
                    x = randint(0, self.width)
                    y = randint(0, self.height)
                    for k in range(multiples):
                        multiples_points[k].append((x, y+k))

                for k in range(multiples):
                    gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[1]:     # Striped Horizontal
            multiples = magnitude // 5
            point_count = 5
            row_count = complexity // 2
            interval_y = (self.height // row_count)
            interval_x = (self.width // point_count)
            row_color_one = cp[randint(0, len(cp)-1)]
            row_color_two = cp[randint(0, len(cp)-1)]

            for i in range(row_count):
                current_color = row_color_one if i % 2 == 0 else row_color_two

                multiples_points = []
                for k in range(multiples):
                    multiples_points.append([])

                for j in range(point_count+2):
                    y_pos = randint(((i-2)*interval_y), ((i+2)*interval_y) )
                    x_pos = randint((j-1)*interval_x, (j*interval_x))
                    for k in range(multiples):
                        multiples_points[k].append((x_pos, y_pos+k))

                for k in range(multiples):
                    gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[2]:     # Striped Vertical
            point_count = 5
            col_count = complexity // 2
            multiples = magnitude // 5
            interval_x = (self.height // col_count) * 2
            interval_y = (self.width // point_count)
            col_color_one = cp[randint(0, len(cp)-1)]
            col_color_two = cp[randint(0, len(cp)-1)]

            for i in range(col_count):
                current_color = col_color_one if i % 2 == 0 else col_color_two

                multiples_points = []
                for k in range(multiples):
                    multiples_points.append([])

                for j in range(point_count+2):
                    y_pos = randint((j-1)*interval_y, j*interval_y)
                    x_pos = randint((i-1)*interval_x, (i+1)*interval_x)
                    for k in range(multiples):
                        multiples_points[k].append((x_pos+k, y_pos))

                for k in range(multiples):
                    gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[3]:     # Mosaic
            row_curve_count = int(complexity // 2)
            row_count = complexity // 3
            x_interval = self.width // row_curve_count
            y_interval = self.height // row_count
            multiples = magnitude // 5
            color_one = cp[randint(0, len(cp) - 1)]
            color_two = cp[randint(0, len(cp) - 1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_curve_count):
                    current_color = color_one if (i + j) % 2 == 0 else color_two
                    x_area = (x_interval * j, x_interval * (j + 1))
                    y_area = (y_interval * i, y_interval * (i + 1))
                    point_count = 4
                    multiples_points = []
                    for m in range(multiples):
                        multiples_points.append([])

                    for k in range(point_count):
                        x = randint(x_area[0], x_area[1])
                        y = randint(y_area[0], y_area[1])
                        for m in range(multiples):
                            multiples_points[m].append((x, y+m))

                    for m in range(multiples):
                        gfxdraw.bezier(layer, multiples_points[m], 5, pg.Color(current_color))

        if style == art_styles_list[4]:     # Cornered
            corner_starts = [((0, self.width//3),(-1, 0)),
                             ((2*self.width//3, self.width),(-1, 0)),
                             ((2*self.width//3, self.width),(self.height, self.height+1)),
                             ((0, self.width//3),(self.height, self.height+1))]
            corner_ends = [((-1, 0),(0, self.height//2)),
                           ((self.width, self.width+1),(0, self.height//2)),
                           ((self.width, self.width+1),(self.height//2, self.height)),
                           ((-1, 0),(self.height//2, self.height))]
            multiples = magnitude // 5
            point_count = 2
            x_area = [0, 0]
            y_area = [0, 0]
            for i in range(complexity//2):
                corner = randint(0, 3)

                if corner == 0: x_area = [0, self.width//3]; y_area = [0, self.height//2]
                if corner == 1: x_area = [2*self.width//3, self.width]; y_area = [0, self.height//2]
                if corner == 2: x_area = [2*self.width//3, self.width]; y_area = [self.height//2, self.height]
                if corner == 3: x_area = [0, self.width//3]; y_area = [self.height//2, self.height]

                current_color = cp[randint(0, len(cp)-1)]

                multiples_points = []
                first_point = (randint(corner_starts[corner][0][0], corner_starts[corner][0][1]),
                               randint(corner_starts[corner][1][0], corner_starts[corner][1][1]))
                last_point = (randint(corner_ends[corner][0][0], corner_ends[corner][0][1]),
                              randint(corner_ends[corner][1][0], corner_ends[corner][1][1]))
                for k in range(multiples):
                    multiples_points.append([first_point])

                for j in range(point_count):
                    x = randint(x_area[0], x_area[1])
                    y = randint(y_area[0], y_area[1])

                    for k in range(multiples):
                        multiples_points[k].append((x+k, y))
                for k in range(multiples):
                    multiples_points[k].append(last_point)

                for k in range(multiples):
                    gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[5]:     # Centered
            curve_count = complexity // 5
            multiples = magnitude // 5
            point_count = 5
            for i in range(curve_count):
                side = randint(0, 3)
                multiples_points = []
                for k in range(multiples):
                    multiples_points.append([(self.width//2, self.height//2)])

                current_color = cp[randint(0, len(cp)-1)]
                x, y = 0, 0
                for j in range(point_count):
                    if side == 0:
                        x = randint(self.width//2+20*j, self.width)
                        y = randint(0, self.height)
                    elif side == 1:
                        x = randint(0, self.width)
                        y = randint(0, self.height // 2 - 20 * j)
                    elif side == 2:
                        x = randint(0, self.width//2-20*j)
                        y = randint(0, self.height)
                    elif side == 3:
                        x = randint(0, self.width)
                        y = randint(self.height // 2 + 20 * j, self.height)

                    for k in range(multiples):
                        multiples_points[k].append((x, y+k))

                for k in range(multiples):
                    gfxdraw.bezier(layer, multiples_points[k], 5, pg.Color(current_color))

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_dots(self, complexity, cp, style, layer, magnitude):
        if style == art_styles_list[0]:     # Chaotic
            for i in range(complexity*20):
                centerX = randint(-25, self.width + 25)
                centerY = randint(-25, self.height + 25)
                current_color = cp[randint(0, len(cp) - 1)]
                pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[1]:     # Striped Horizontal
            row_dot_count = complexity * 2
            row_count = complexity // 2
            interval = self.height // row_count
            row_colour_one = cp[randint(0, len(cp) - 1)]
            row_colour_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count+1):
                for j in range(row_dot_count):
                    current_color = row_colour_one if i % 2 == 0 else row_colour_two
                    centerY = i * interval + 5
                    centerX = randint(0, self.width)
                    pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[2]:     # Striped Vertical
            row_dot_count = complexity * 2
            row_count = complexity // 2
            interval = self.width // row_count
            row_colour_one = cp[randint(0, len(cp) - 1)]
            row_colour_two = cp[randint(0, len(cp) - 1)]
            while row_colour_two == row_colour_one:
                row_colour_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count+1):
                for j in range(row_dot_count):
                    current_color = row_colour_one if i % 2 == 0 else row_colour_two
                    centerX = i * interval + 5
                    centerY = randint(0, self.width)
                    pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[3]:     # Mosaic
            row_dot_count = complexity * 5
            interval = self.width // row_dot_count * 2
            row_count = self.height // interval + 5
            color_one = cp[randint(0, len(cp)-1)]
            color_two = cp[randint(0, len(cp)-1)]
            while color_two == color_one:
                color_two = cp[randint(0, len(cp) - 1)]
            for i in range(row_count):
                for j in range(row_dot_count):
                    current_color = color_one if (i+j) % 2 == 0 else color_two
                    centerX = 2 + j * interval
                    centerY = 2 + i * interval
                    pg.draw.circle(layer, pg.Color(current_color), (centerX, centerY), magnitude[1]//30 + 2)

        if style == art_styles_list[4]:     # Cornered
            for i in range(complexity * 8):
                current_color = cp[randint(0, len(cp) - 1)]
                corner = randint(0, 3)
                x_area, y_area = (0, 0), (0, 0)
                if corner == 0:
                    x_area, y_area = (0, self.width // 3), (0, self.height // 3)
                if corner == 1:
                    x_area, y_area = (self.width // 1.5, self.width), (0, self.height // 3)
                if corner == 2:
                    x_area, y_area = (self.width // 1.5, self.width), (self.height // 1.5, self.height)
                if corner == 3:
                    x_area, y_area = (0, self.width // 3), (self.height // 1.5, self.height)

                posX = randint(x_area[0], x_area[1])
                posY = randint(y_area[0], y_area[1])

                pg.draw.circle(layer, pg.Color(current_color), (posX, posY), magnitude[1]//30 + 2)

        if style == art_styles_list[5]:     # Centered
            in_x_area, in_y_area = (self.width // 4, 3 * self.width // 4), (self.height // 4, 3 * self.height // 4)
            out_x_area, out_y_area = (self.width // 6, 5 * self.width // 6), (self.height // 6, 5 * self.height // 6)

            for i in range(complexity * 4):
                random_number = randint(0, 5)
                if random_number < 4:
                    center_x = randint(in_x_area[0], in_x_area[1])
                    center_y = randint(in_y_area[0], in_y_area[1])
                else:
                    center_x = randint(out_x_area[0], out_x_area[1])
                    center_y = randint(out_y_area[0], out_y_area[1])

                current_color = cp[randint(0, len(cp) - 1)]
                pg.draw.circle(layer, pg.Color(current_color), (center_x, center_y), magnitude[1]//30 + 2)

        if style == art_styles_list[6]:     # Empty
            pass

    def generate_bg(self, color):
        self.bg_layer.fill(pg.Color(color))

    def generate_fg(self, overlay):
        self.clean_layer(self.fg_layer)
        self.fg_layer.blit(overlay, (0, 0))
        self.blit_to_canvas()

    def generate_layer_one(self, art_style, art_shape, color_palette, complexity, magnitude):
        self.generate_art(self.layer_one, art_style, art_shape, color_palette, complexity, magnitude)

    def generate_layer_two(self, art_style, art_shape, color_palette, complexity, magnitude):
        self.generate_art(self.layer_two, art_style, art_shape, color_palette, complexity, magnitude)

    def generate_art(self, layer, art_style, art_shape, color_palette, complexity, magnitude):
        self.clean_layer(layer)
        layer.set_colorkey((0, 0, 0))

        if art_shapes_list[0] == art_shape:
            self.generate_lines(complexity, color_palette, art_style, layer, magnitude)

        if art_shapes_list[1] == art_shape:
            self.generate_circles(complexity, color_palette, art_style, layer, magnitude, 0)

        if art_shapes_list[2] == art_shape:
            self.generate_squares(complexity, color_palette, art_style, layer, magnitude)

        if art_shapes_list[3] == art_shape:
            self.generate_polygons(complexity, color_palette, art_style, layer, magnitude, 1)

        if art_shapes_list[4] == art_shape:
            self.generate_polygons(complexity, color_palette, art_style, layer, magnitude, 0)

        if art_shapes_list[5] == art_shape:
            self.generate_dots(complexity, color_palette, art_style, layer, magnitude)

        if art_shapes_list[6] == art_shape:
            self.generate_curves(complexity, color_palette, art_style, layer, magnitude[1])

        if art_shapes_list[7] == art_shape:
            self.generate_circles(complexity, color_palette, art_style, layer, magnitude, 1)

    def blit_to_canvas(self):
        self.canvas.blit(self.bg_layer, (0, 0))
        self.canvas.blit(self.layer_one, (0, 0))
        self.canvas.blit(self.layer_two, (0, 0))
        self.canvas.blit(self.fg_layer, (0, 0))

    def save(self, filename:str):
        pg.init()
        self.blit_to_canvas()
        pg.image.save(self.canvas, f"{filename}.png")
        pg.quit()