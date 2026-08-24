"""Calculator practice module — used by Lessons 2, 3, and 7."""


class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(result)
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(result)
        return result

    def divide(self, a, b):
        if b == 0:
            raise Exception("Cannot divide by zero")
        result = a / b
        self.history.append(result)
        return result

    def clear_history(self):
        self.history = []

    def average(self):
        # TODO: guard against empty history (ZeroDivisionError)
        return sum(self.history) / len(self.history)


class Person:
    """Macro-practice target: attributes need a `self.` prefix (Lesson 3.2)."""

    def __init__(self):
        name = ""
        age = 0
        email = ""
        phone = ""
        address = ""
