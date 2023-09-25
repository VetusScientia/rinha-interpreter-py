import ujson
import sys
from enum import Enum


class BinaryOp(Enum):
    Add = "Add"
    Sub = "Sub"
    Mul = "Mul"
    Div = "Div"
    Rem = "Rem"
    Eq = "Eq"
    Neq = "Neq"
    Lt = "Lt"
    Gt = "Gt"
    Lte = "Lte"
    Gte = "Gte"
    And = "And"
    Or = "Or"


def add(x, y):
    if type(x) == str or type(y) == str:
        return str(x) + str(y)
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

tail_call_recursion = False


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

