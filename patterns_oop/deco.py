class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,          # health points
            "MP": 42,           # magic points
            "SP": 100,          # skill points
            "Strength": 15,     # сила
            "Perception": 4,    # восприятие
            "Endurance": 8,     # выносливость
            "Charisma": 2,      # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,       # ловкость
            "Luck": 1           # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero):
    def __init__(self, base):
        super().__init__()
        self.base = base

    def get_positive_effects(self):
        res = self.base.get_positive_effects()
        return res

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    def get_stats(self):
        return self.base.get_stats()


class AbstractPositive(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [self.__class__.__name__]


class AbstractNegative(AbstractEffect):

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]


class Berserk(AbstractPositive):
    def get_stats(self):
        self.stats = self.base.get_stats()
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
        self.stats = self.base.get_stats()
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
        self.stats = self.base.get_stats()
        change_stats = {
            "Strength": 4,      # сила
            "Endurance": 4,     # выносливость
            "Agility": 4,       # ловкость
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()


class EvilEye(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()
        change_stats = {
            "Luck": -10           # удача
        }
        for stat in change_stats:
            self.stats[stat] += change_stats[stat]
        return self.stats.copy()


class Curse(AbstractNegative):
    def get_stats(self):
        self.stats = self.base.get_stats()
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



hero = Hero()
print(hero.get_stats())
print(hero.stats)
print(hero.get_negative_effects())
print(hero.get_positive_effects())
brs1 = Berserk(hero)
print(brs1.get_stats())
print(brs1.get_negative_effects())
print(brs1.get_positive_effects())
brs2 = Berserk(brs1)
cur1 = Curse(brs2)
print(cur1.get_stats())
print(cur1.get_positive_effects())
print(cur1.get_negative_effects())
cur1.base = brs1
print(cur1.get_stats())
print(cur1.get_positive_effects())
print(cur1.get_negative_effects())
