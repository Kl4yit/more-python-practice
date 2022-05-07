class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, obj_type):
        if obj_type is int:
            self.event = ('IntHandler', None)
        if obj_type is float:
            self.event = ('FloatHandler', None)
        if obj_type is str:
            self.event = ('StrHandler', None)


class EventSet:
    def __init__(self, obj_type):
        if type(obj_type) == int:
            self.event = ('IntHandler', obj_type)
        if type(obj_type) == float:
            self.event = ('FloatHandler', obj_type)
        if type(obj_type) == str:
            self.event = ('StrHandler', obj_type)


class NullHandler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, obj, event):
        if self.successor is not None:
            return self.successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.event[0] == self.__class__.__name__:
            if event.event[1] is None:
                return obj.integer_field
            else:
                obj.integer_field = event.event[1]
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.event[0] == self.__class__.__name__:
            if event.event[1] is None:
                return obj.string_field
            else:
                obj.string_field = event.event[1]
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.event[0] == self.__class__.__name__:
            if event.event[1] is None:
                return obj.float_field
            else:
                obj.float_field = event.event[1]
        else:
            return super().handle(obj, event)



# obj = SomeObject()
# obj.integer_field = 42
# obj.float_field = 3.14
# obj.string_field = "some text"
# chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
# print(chain.handle(obj, EventGet(int)))
# print(chain.handle(obj, EventGet(float)))
# print(chain.handle(obj, EventGet(str)))
# chain.handle(obj, EventSet(100))
# print(chain.handle(obj, EventGet(int)))
# chain.handle(obj, EventSet(0.5))
# print(chain.handle(obj, EventGet(float)))
# chain.handle(obj, EventSet('new text'))
# print(chain.handle(obj, EventGet(str)))
