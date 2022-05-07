import math

import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        self.game_engine = None
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    # connect_engine
    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def draw_hero(self):
        self.game_engine.hero.draw(self)

    def get_min_coors(self):
        hero_pos = self.game_engine.hero.position
        width_rem = math.ceil(self.get_width() / self.game_engine.sprite_size)
        height_rem = math.ceil(self.get_height() / self.game_engine.sprite_size)
        right_wall = hero_pos[0] >= len(self.game_engine.map[0]) - math.ceil(width_rem / 2)
        left_wall = hero_pos[0] <= math.ceil(width_rem / 2)
        lower_wall = hero_pos[1] >= len(self.game_engine.map) - math.ceil(height_rem / 2)
        upper_wall = hero_pos[1] <= math.ceil(height_rem / 2)
        if left_wall:
            min_x = 0
        elif right_wall:
            min_x = len(self.game_engine.map[0]) - width_rem
        else:
            min_x = hero_pos[0] - math.ceil(width_rem / 2)

        if upper_wall:
            min_y = 0
        elif lower_wall:
            min_y = len(self.game_engine.map) - height_rem
        else:
            min_y = hero_pos[1] - math.ceil(height_rem / 2)
        return [min_x, min_y, width_rem, height_rem]

    def draw_map(self):

        # FIXME || calculate (min_x,min_y) - left top corner
        ###################################################################################
        viewport = self.get_min_coors()
        ####################################################################################

        # min_x = 0
        # min_y = 0

    ##

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - viewport[0]):
                for j in range(len(self.game_engine.map) - viewport[1]):
                    self.blit(
                        self.game_engine.map[viewport[1] + j][viewport[0] + i][0],
                        (
                            i * self.game_engine.sprite_size,
                            j * self.game_engine.sprite_size
                        )
                    )
        else:
            self.fill(colors["white"])

    def draw_objects(self):
        size = self.game_engine.sprite_size
    # FIXME || calculate (min_x,min_y) - left top corner

        viewport = self.get_min_coors()

        for obj in self.game_engine.objects:
            is_in_screen = viewport[0] <= obj.position[0] <= viewport[0] + viewport[2] and viewport[1] <= obj.position[1] <= viewport[1] + viewport[3]
            if is_in_screen:
                self.blit(obj.sprite[0], ((obj.position[0] - viewport[0]) * size,
                                          (obj.position[1] - viewport[1]) * size))

    def draw(self, canvas):
        size = self.game_engine.sprite_size
        # FIXME || calculate (min_x,min_y) - left top corner
        ###################################################################

        min_x = 0
        min_y = 0
        ####################################################################
        ##

        self.draw_map()
        self.draw_objects()
        self.draw_hero()
        super().draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        self.game_engine = None
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors["red"], (50, 30, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70, 200 * self.game_engine.hero.exp / (100 * (2 ** (self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["black"]), (250, 0))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["black"]), (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]), (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]), (10, 70))

        self.blit(font.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.game_engine.hero.exp}/{(100 * (2 ** (self.game_engine.hero.level - 1)))}', True, colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["black"]),
                  (550, 70))

        super().draw(canvas)
    # draw next surface in chain


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        super().draw(canvas)

    # FIXME
    # draw next surface in chain

    def connect_engine(self, engine):
        engine.subscribe(self)
        super().connect_engine(engine)
        #  set this class as Observer to engine and send it to next in
        # chain


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_engine = None
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
    # FIXME You can add some help information

    # def connect_engine(self, engine):
    #     # save engine and send it to next in chain

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.game_engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))
        super().draw(canvas)
    # FIXME
    # draw next surface in chain


class OverWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_engine = None
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append(["GAME", "OVER"])
        self.data.append([" R ", "Restart Game"])
    # FIXME You can add some help information

    # def connect_engine(self, engine):
    #     # save engine and send it to next in chain

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.game_over:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.game_engine.game_over:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font2.render(text[0], True, ((128, 128, 255))),
                          (250, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (350, 50 + 30 * i))
        super().draw(canvas)
    # FIXME
    # draw next surface in chain
