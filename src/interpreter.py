import numpy as np
import ujson
from utils import *

def interpret_int(node, environment):
    value = node.get("value", 0)
    return np.int32(value)


def interpret_str(node, environment):
    return node["value"]


def interpret_bool(node, environment):
    return node["value"]


def interpret_binary(node, environment):
    lhs = interpret(node.get("lhs", node), environment)
    rhs = interpret(node.get("rhs", node), environment)
    op = node["op"]
    operators = {
        "Add": add,
        "Sub": sub,
        "Mul": mul,
        "Div": div,
        "Rem": rem,
        "Eq": eq,
        "Neq": neq,
        "Lt": lt,
        "Gt": gt,
        "Lte": lte,
        "Gte": gte,
        "And": and_,
        "Or": or_
    }
    if op == "Div" and rhs == 0:
        raise RinhaError("Division by zero")
    if op in operators:
        return operators[op](lhs, rhs)
    else:
        raise RinhaError(f"Unsupported operator: {op}")


def interpret_let(node, environment):
    name = node["name"]["text"]
    new_environment = environment.copy()
    value = interpret(node["value"], new_environment)
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


def interpret_closure(node, environment):
    return Closure(node, environment)


def optimize_tail_call(func_node, func_environment, args):
    global tail_call_recursion
    if func_node == tail_call_recursion:
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

        return result


def interpret_function(node, environment):
    return interpret_closure(node, environment)


def interpret_call(node, environment):
    global tail_call_recursion
    callee = interpret(node["callee"], environment)
    args = [interpret(arg, environment) for arg in node["arguments"]]

    if isinstance(callee, Closure):
        func_node = callee.func_node
        func_environment = callee.environment.copy()
        for param, arg in zip(func_node["parameters"], args):
            func_environment[param["text"]] = arg

        if tail_call_recursion and func_node == tail_call_recursion:
            return optimize_tail_call(func_node, func_environment, args)
        else:
            custom_stack.push(func_node, func_environment)
            while not custom_stack.is_empty():
                func_node, func_environment = custom_stack.pop()
                result = interpret(func_node["value"], func_environment)

            tail_call_recursion = False

            return result
    else:
        call_key = (callee["kind"], tuple(args))

        if call_key in cache:
            return cache[call_key]
        else:
            if callee["kind"] == "Function":
                func_environment = environment.copy()
                for param, arg in zip(callee["parameters"], args):
                    func_environment[param["text"]] = arg

                result = interpret(callee["value"], func_environment)

                cache[call_key] = result

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

