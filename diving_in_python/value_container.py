
class Value:
    def __get__(self, instance, owner):
        if owner == Account:
            return instance.curr_amount

    def __set__(self, instance, value):
        instance.curr_amount = value - (value * instance.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


