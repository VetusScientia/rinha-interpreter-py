import ujson
from enum import Enum

tail_call_recursion = False

def add(x, y):
    if type(x) == str or type(y) == str:
        return str(x) + str(y)
    if x is None or y is None:
        return None
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    return int(x / y)

def rem(x, y):
    return x % y

def eq(x, y):
    return x == y

def neq(x, y):
    return x != y

def lt(x, y):
    return x < y

def gt(x, y):
    return x > y

def lte(x, y):
    return x <= y

def gte(x, y):
    return x >= y

def and_(x, y):
    return x and y

def or_(x, y):
    return x or y


class RinhaError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Closure:
    def __init__(self, func_node, environment):
        self.func_node = func_node
        self.environment = environment


class CustomStack:
    def __init__(self):
        self.frames = []

    def push(self, func_node, environment):
        self.frames.append((func_node, environment))

    def pop(self):
        return self.frames.pop()

    def is_empty(self):
        return len(self.frames) == 0


custom_stack = CustomStack()


class CustomStack:
    def __init__(self):
        self.frames = []

    def push(self, func_node, environment):
        self.frames.append((func_node, environment))

    def pop(self):
        return self.frames.pop()

    def is_empty(self):
        return len(self.frames) == 0


binary_operators = {
    "Add": lambda x, y: str(x) + str(y) if type(x) == str or type(y) == str else x + y,
    "Sub": lambda x, y: x - y,
    "Mul": lambda x, y: x * y,
    "Div": lambda x, y: int(x / y) if y != 0 else None,
    "Rem": lambda x, y: x % y,
    "Eq": lambda x, y: x == y,
    "Neq": lambda x, y: x != y,
    "Lt": lambda x, y: x < y,
    "Gt": lambda x, y: x > y,
    "Lte": lambda x, y: x <= y,
    "Gte": lambda x, y: x >= y,
    "And": lambda x, y: x and y,
    "Or": lambda x, y: x or y
}


def format_output(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, Closure):
        return "<#closure>"
    elif isinstance(value, tuple):
        return f"({format_output(value[0])}, {format_output(value[1])})"
    elif isinstance(value, dict):
        return ujson.dumps(value)
    elif value is None:
        return "null"
    else:
        return value


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return ujson.load(file)

