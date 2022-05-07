from abc import ABC, abstractmethod


class Creature(ABC):
    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def feed(self):
        ...

    @abstractmethod
    def make_noise(self):
        ...


class Animal(Creature):

    def move(self):
        print('i move forward')

    def feed(self):
        print('i eat grass')

    def make_noise(self):
        print('wooo')


class AbstractDecorator(Creature):
    def __init__(self, base):
        self.base = base

    def move(self):
        self.base.move()

    def feed(self):
        self.base.feed()

    def make_noise(self):
        self.base.make_noise()


class Swimming(AbstractDecorator):
    def move(self):
        print('i swim')

    def make_noise(self):
        print('...')


class Fast(AbstractDecorator):
    def move(self):
        self.base.move()
        print('fast')


class Predator(AbstractDecorator):
    def feed(self):
        print('i eat other animals')



animal = Animal()
animal.feed()
animal.move()
animal.make_noise()
print()

swimming = Swimming(animal)
swimming.feed()
swimming.move()
swimming.make_noise()
print()

pred = Predator(swimming)
pred.feed()
pred.move()
pred.make_noise()
print()

fast = Fast(pred)
fast.feed()
fast.move()
fast.make_noise()

# fast.base.base.base = fast.base

print(fast.base)
print(fast.base.base)
print(fast.base.base.base)
print(fast.base.base.base.base)
print(fast.base.base.base.base.base)

fast.feed()
fast.move()
fast.make_noise()
