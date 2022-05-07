from abc import ABC, abstractmethod
import numpy as np
import pygame
import random


class AbstractObject(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def draw(self, display):
        ...


class Interactive(ABC):
    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):
    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)

    def draw(self, display):
        display.blit(
            self.sprite,
            (
                self.position[0] * display.game_engine.sprite_size,
                self.position[1] * display.game_engine.sprite_size,
            )
        )


class Creature(AbstractObject):
    def __init__(self, icon, stats, position):
        self.max_hp = None
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def draw(self, display):
        display.blit(
            self.sprite,
            (
                self.position[0] * display.game_engine.sprite_size,
                self.position[1] * display.game_engine.sprite_size,
            )
        )


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp

    def draw(self, display):
        viewport = display.get_min_coors()
        display.blit(
            self.sprite,
            (
                (self.position[0] - viewport[0]) * display.game_engine.sprite_size,
                (self.position[1] - viewport[1]) * display.game_engine.sprite_size,
            )
        )


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, exp, position):
        super().__init__(icon, stats, position)
        self.exp = exp

    def interact(self, engine, hero):
        sts = ['strength', 'endurance', 'intelligence', 'luck'][np.random.randint(0, 4)]
        damage = self.hp
        enemy_luck = False if np.random.randint(0, 2) == 0 else True
        if hero.stats[sts] <= self.stats[sts] or enemy_luck:
            hero.hp -= damage
        hero.exp += self.exp
        engine.notify(f"Enemy {self.stats['name']} exhausted!")
        engine.new_level()


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def stats(self):
        return self.base.stats

    @stats.setter
    def stats(self, value):
        self.base.stats = value

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @sprite.setter
    def sprite(self, value):
        self.base.sprite = value

    @abstractmethod
    def apply_effect(self):
        pass


#
# add classes


class Berserk(Effect):
    def apply_effect(self):
        change_stats = {
            "strength": 7,
            "endurance": 7,
            "intelligence": -3,
            "luck": 7
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        self.hp += 5


class Blessing(Effect):
    def apply_effect(self):
        change_stats = {
            "strength": 2,
            "endurance": 2,
            "intelligence": 2,
            "luck": 2
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]


class Weakness(Effect):
    def apply_effect(self):
        change_stats = {
            "strength": -4,
            "endurance": -4,
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
