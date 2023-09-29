import sys
sys.setrecursionlimit(10000)

class Location:
    def __init__(self, start, end, filename):
        self.start = start
        self.end = end
        self.filename = filename

class Parameter:
    def __init__(self, text, location):
        self.text = text
        self.location = location

class Var:
    def __init__(self, kind, text, location):
        self.kind = kind
        self.text = text
        self.location = location

class Function:
    def __init__(self, kind, parameters, value, location, closure_env):
        self.kind = kind
        self.parameters = parameters
        self.value = value
        self.location = location
        self.closure_env = closure_env

    def evaluate(self, env):
        return self

class Call:
    def __init__(self, kind, callee, arguments, location):
        self.kind = kind
        self.callee = callee
        self.arguments = arguments
        self.location = location

class Let:
    def __init__(self, kind, name, value, next_term, location):
        self.kind = kind
        self.name = name
        self.value = value
        self.next_term = next_term
        self.location = location

class Str:
    def __init__(self, kind, value, location):
        self.kind = kind
        self.value = value
        self.location = location

class Int:
    def __init__(self, kind, value, location):
        self.kind = kind
        self.value = value
        self.location = location

class BinaryOp:
    def __init__(self, kind):
        self.kind = kind

class Binary:
    def __init__(self, kind, lhs, op, rhs, location):
        self.kind = kind
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.location = location

class Tuple:
    def __init__(self, kind, first, second, location):
        self.kind = kind
        self.first = first
        self.second = second
        self.location = location

class First:
    def __init__(self, kind, value, location):
        self.kind = kind
        self.value = value
        self.location = location

class Second:
    def __init__(self, kind, value, location):
        self.kind = kind
        self.value = value
        self.location = location

class Bool:
    def __init__(self, kind, value, location):
        self.kind = kind
        self.value = value
        self.location = location

class If:
    def __init__(self, kind, condition, then, otherwise, location):
        self.kind = kind
        self.condition = condition
        self.then = then
        self.otherwise = otherwise
        self.location = location

class Print:
    def __init__(self, kind, value, location):
        self.kind = kind
        self.value = value
        self.location = location

class File:
    def __init__(self, name, expression, location):
        self.name = name
        self.expression = expression
        self.location = location

class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache = {}

    def is_empty(self):
        return len(self.cache) == 0

cache = Cache()