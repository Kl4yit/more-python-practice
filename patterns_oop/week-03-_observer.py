from abc import ABC, abstractmethod


class ObservableEngine(Engine):
    def __init__(self):
        super().__init__()
        self.__subscribers = set()

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber)

    def notify(self, achievement):
        for sub in self.__subscribers:
            sub.update(achievement)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, achieve):
        ...


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, achieve):
        self.achievements.add(achieve['title'])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = []

    def update(self, achieve):
        self.achievements += [achieve] if achieve not in self.achievements else []
