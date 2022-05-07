from abc import ABC, abstractmethod


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.get_stats()

    @abstractmethod
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        return self.base.get_stats()


class AbstractPositive(AbstractEffect, ABC):

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [self.__class__.__name__]

    def get_negative_effects(self):
        return super().get_negative_effects()

    @abstractmethod
    def get_stats(self):
        super().get_stats()


class AbstractNegative(AbstractEffect, ABC):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]

    def get_positive_effects(self):
        return super().get_positive_effects()

    @abstractmethod
    def get_stats(self):
        super().get_stats()


class Berserk(AbstractPositive):
    def get_stats(self):
        change_stats = {
            "HP": 50,           # health points
            "Strength": 7,      # сила
            "Endurance": 7,     # выносливость
            "Agility": 7,       # ловкость
            "Luck": 7,          # удача
            "Charisma": -3,     # харизма
            "Intelligence": -3, # интеллект
            "Perception": -3    # восприятие
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()


class Blessing(AbstractPositive):
    def get_stats(self):
        change_stats = {
            "Strength": 2,      # сила
            "Perception": 2,    # восприятие
            "Endurance": 2,     # выносливость
            "Charisma": 2,      # харизма
            "Intelligence": 2,  # интеллект
            "Agility": 2,       # ловкость
            "Luck": 2           # удача
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()


class Weakness(AbstractNegative):
    def get_stats(self):
        change_stats = {
            "Strength": -4,      # сила
            "Endurance": -4,     # выносливость
            "Agility": -4,       # ловкость
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()


class EvilEye(AbstractNegative):
    def get_stats(self):
        change_stats = {
            "Luck": -10           # удача
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()


class Curse(AbstractNegative):
    def get_stats(self):
        change_stats = {
            "Strength": -2,      # сила
            "Perception": -2,    # восприятие
            "Endurance": -2,     # выносливость
            "Charisma": -2,      # харизма
            "Intelligence": -2,  # интеллект
            "Agility": -2,       # ловкость
            "Luck": -2           # удача
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()

