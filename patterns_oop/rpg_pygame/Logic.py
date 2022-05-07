import Service


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    level_list_max = None
    subscribers = set()
    score = 0.
    working = True
    game_process = True
    show_help = False
    game_over = False

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                self.delete_object(obj)
                obj.interact(self, self.hero)
                if len(self.objects) == 0 and self.level < self.level_list_max:
                    Service.open_next_dungeon(self)
                if self.hero.hp <= 0:
                    self.hero.hp = 0
                    Service.game_over(self)
                    # MOVEMENT
    def move_up(self):
        self.score -= 0.02
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] -= 1
        self.interact()

    def move_down(self):
        self.score -= 0.02
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] += 1
        self.interact()

    def move_left(self):
        self.hero.sprite = self.hero.stats['sprite_left']
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.position[0] -= 1
        self.interact()

    def move_right(self):
        self.hero.sprite = self.hero.stats['sprite_right']
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.position[0] += 1
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)

    def new_level(self):
        counter = self.hero.level_up()
        for it in counter:
            self.notify(it)
