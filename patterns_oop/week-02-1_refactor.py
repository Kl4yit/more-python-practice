import math
import random

import pygame


SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, dot):
        self.x = dot[0]
        self.y = dot[1]

    def __add__(self, other):
        return Vec2d((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vec2d((self.x - other.x, self.y - other.y))

    def __mul__(self, other):
        return Vec2d((self.x * other, self.y * other))

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def int_pair(self):
        res = (int(self.x), int(self.y))
        return res


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_dot_and_velocity(self, dot, vel=None):
        self.points.append(Vec2d(dot))
        self.speeds.append(Vec2d(vel)) if vel else ...

    def set_points(self, count,  points=None):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x = -self.speeds[p].x
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y = -self.speeds[p].y

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 self.points[p_n].int_pair,
                                 self.points[p_n + 1].int_pair, width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair, width)


class Knot(Polyline):
    def set_points(self, count, points=None):
        self.get_knot(points, count)

    def add_dot_and_count(self, dot, count):
        self.add_dot_and_velocity(dot, count)

    def add_dot_and_velocity(self, dot, vel=None):
        self.get_knot(dot, vel)

    def get_knot(self, points, count):
        if len(points) < 3:
            return
        res = []
        for i in range(-2, len(points) - 2):
            ptn = [
                points[i] * 0.5 + points[i + 1] * 0.5,
                points[i + 1],
                points[i + 1] * 0.5 + points[i + 2] * 0.5
            ]
            res.extend(self.get_points(ptn, count))
        self.points = res

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    @staticmethod
    def get_point(points, alpha):
        buff = (points[1] * alpha) + (points[0] * (1 - alpha))
        return (points[2] * alpha) + (buff * (1 - alpha))


class Draw:
    @staticmethod
    def draw_help():
        """функция отрисовки экрана справки программы"""
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [
            ["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["F", "Faster"],
            ["D", "Slower"],
            ["", ""],
            [str(steps), "Current points"],
            [str(fps), "FPS"]
        ]
        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    clock = pygame.time.Clock()
    steps = 35
    fps = 60
    working = True
    points = Polyline()
    knot = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = Polyline()
                    knot = Knot()
                if event.key == pygame.K_f:
                    fps += 10
                if event.key == pygame.K_d:
                    fps -= 10 if fps > 10 else 0
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.add_dot_and_velocity(
                    event.pos,
                    (random.random() * 2, random.random() * 2)
                )

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        points.draw_points()
        knot.set_points(steps, points.points)
        knot.draw_points("line", 3, color)
        if not pause:
            points.set_points(count=steps)
        if show_help:
            Draw.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
