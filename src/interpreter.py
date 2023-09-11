from rinha_error import *
from format_output import *
from sympy import symbols

MAX_CACHE_SIZE = 200

cache = {}

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

def limit_cache_size():
    while len(cache) > MAX_CACHE_SIZE:
        cache.pop(next(iter(cache)))

def interpret_str(node, environment):
    return node["value"]

def interpret_bool(node, environment):
    return node["value"]

def interpret_binary(node, environment):
    lhs = interpret(node.get("lhs", node), environment)
    rhs = interpret(node.get("rhs", node), environment)
    op = node["op"]
    operators = {
        "Add": lambda x, y: str(x) + str(y) if isinstance(x, str) or isinstance(y, str) else x + y,
        "Sub": lambda x, y: x - y,
        "Mul": lambda x, y: x * y,
        "Div": lambda x, y: x // y if y != 0 else None,
        "Rem": lambda x, y: x % y if y != 0 else None,
        "Eq": lambda x, y: x == y,
        "Neq": lambda x, y: x != y,
        "Lt": lambda x, y: x < y,
        "Gt": lambda x, y: x > y,
        "Lte": lambda x, y: x <= y,
        "Gte": lambda x, y: x >= y,
        "And": lambda x, y: x and y,
        "Or": lambda x, y: x or y
    }
    if op == "Div" and rhs == 0:
        raise RinhaError("Division by zero")

    if op in operators:
        return operators[op](lhs, rhs)
    else:
        raise RinhaError(f"Unsupported operator: {op}")

def interpret_let(node, environment):
    name = node["name"]["text"]
    value = interpret(node["value"], environment)
    new_environment = environment.copy()
    new_environment[name] = value
    return interpret(node.get("next", node), new_environment)

def interpret_if(node, environment):
    condition = interpret(node["condition"], environment)
    return interpret(node["then"] if condition else node["otherwise"], environment)

def interpret_print(node, environment):
    value = interpret(node["value"], environment)
    output = format_output(value)
    if isinstance(output, tuple):
        output = ", ".join(str(val) for val in output)
    return output

tail_call_recursion = False

def interpret_function(node, environment):
    return Closure(node, environment)

custom_stack = CustomStack()

def interpret_call(node, environment):
    global tail_call_recursion
    callee = interpret(node["callee"], environment)
    args = [interpret(arg, environment) for arg in node["arguments"]]

    func_node = callee.func_node if isinstance(callee, Closure) else callee
    call_key = (func_node["kind"], tuple(args))

    if call_key in cache:
        return cache[call_key]
    else:
        if func_node["kind"] == "Function":
            if "name" not in func_node:
                func_environment = environment.copy()
                for param, arg in zip(func_node["parameters"], args):
                    func_environment[param["text"]] = arg

                if tail_call_recursion and func_node == tail_call_recursion:
                    while True:
                        result = interpret(func_node["value"], func_environment)
                        if not callable(result):
                            return result
                else:
                    custom_stack.push(func_node, func_environment)
                    while not custom_stack.is_empty():
                        func_node, func_environment = custom_stack.pop()
                        result = interpret(func_node["value"], func_environment)

                    tail_call_recursion = False

                    cache[call_key] = result
                    limit_cache_size()
                    return result

def interpret_first(node, environment):
    tuple_value = interpret(node["value"], environment)
    if isinstance(tuple_value, tuple):
        return tuple_value[0]
    else:
        raise RinhaError(f"Expected a tuple, got {type(tuple_value).__name__}")

def interpret_second(node, environment):
    tuple_value = interpret(node["value"], environment)
    if isinstance(tuple_value, tuple):
        return tuple_value[1]
    else:
        raise RinhaError(f"Expected a tuple, got {type(tuple_value).__name__}")

def interpret_tuple(node, environment):
    first = interpret(node["first"], environment)
    second = interpret(node["second"], environment)
    return (first, second)

def interpret_var(node, environment):
    var_name = node["text"]
    if var_name in environment:
        return environment[var_name]
    else:
        raise RinhaError(f"Variable '{var_name}' not defined")

def interpret_parameter(node, environment):
    return node

def interpret_int(node, environment):
    value = node.get("value", 0)
    return value

def interpret(node, environment):
    try:
        if isinstance(node, dict):
            kind = node.get("kind")
            interpreter = {
                "Int": interpret_int,
                "Str": interpret_str,
                "Bool": interpret_bool,
                "Binary": interpret_binary,
                "Let": interpret_let,
                "If": interpret_if,
                "Print": interpret_print,
                "Function": interpret_function,
                "Call": interpret_call,
                "First": interpret_first,
                "Second": interpret_second,
                "Tuple": interpret_tuple,
                "Var": interpret_var,
                "Parameter": interpret_parameter
            }
            result = interpreter[kind](node, environment) if kind in interpreter else None
            return result if result is not None else None
        return node
    except RinhaError as e:
        print(f"RinhaError: {e}")
