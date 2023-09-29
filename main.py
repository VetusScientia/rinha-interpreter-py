import json
import numpy as np
from utils import *

def load_json_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        return json.load(file)

def parse_json_to_ast(json_data):
    def parse_location(location_data):
        return Location(location_data['start'], location_data['end'], location_data['filename'])

    def parse_parameter(parameter_data):
        return Parameter(parameter_data['text'], parse_location(parameter_data['location']))

    def parse_var(var_data):
        return Var(var_data['kind'], var_data['text'], parse_location(var_data['location']))

    def parse_function(function_data):
        parameters = [parse_parameter(p) for p in function_data['parameters']]
        return Function(
            function_data['kind'],
            parameters,
            parse_term(function_data['value']),
            parse_location(function_data['location']),
            {}
        )

    def parse_call(call_data):
        return Call(call_data['kind'], parse_term(call_data['callee']), [parse_term(arg) for arg in call_data['arguments']], parse_location(call_data['location']))

    def parse_let(let_data):
        return Let(let_data['kind'], parse_parameter(let_data['name']), parse_term(let_data['value']), parse_term(let_data['next']), parse_location(let_data['location']))

    def parse_str(str_data):
        return Str(str_data['kind'], str_data['value'], parse_location(str_data['location']))

    def parse_int(int_data):
        return Int(int_data['kind'], int_data['value'], parse_location(int_data['location']))

    def parse_binary(binary_data):
        return Binary(binary_data['kind'], parse_term(binary_data['lhs']), BinaryOp(binary_data['op']), parse_term(binary_data['rhs']), parse_location(binary_data['location']))

    def parse_tuple(tuple_data):
        return Tuple(tuple_data['kind'], parse_term(tuple_data['first']), parse_term(tuple_data['second']), parse_location(tuple_data['location']))

    def parse_first(first_data):
        return First(first_data['kind'], parse_term(first_data['value']), parse_location(first_data['location']))

    def parse_second(second_data):
        return Second(second_data['kind'], parse_term(second_data['value']), parse_location(second_data['location']))

    def parse_bool(bool_data):
        return Bool(bool_data['kind'], bool_data['value'], parse_location(bool_data['location']))

    def parse_if(if_data):
        return If(if_data['kind'], parse_term(if_data['condition']), parse_term(if_data['then']), parse_term(if_data['otherwise']), parse_location(if_data['location']))

    def parse_print(print_data):
        return Print(print_data['kind'], parse_term(print_data['value']), parse_location(print_data['location']))

    def parse_term(term_data):
        kind = term_data['kind']
        if kind == 'Var':
            return parse_var(term_data)
        elif kind == 'Function':
            return parse_function(term_data)
        elif kind == 'Call':
            return parse_call(term_data)
        elif kind == 'Let':
            return parse_let(term_data)
        elif kind == 'Str':
            return parse_str(term_data)
        elif kind == 'Int':
            return parse_int(term_data)
        elif kind == 'Binary':
            return parse_binary(term_data)
        elif kind == 'Tuple':
            return parse_tuple(term_data)
        elif kind == 'First':
            return parse_first(term_data)
        elif kind == 'Second':
            return parse_second(term_data)
        elif kind == 'Bool':
            return parse_bool(term_data)
        elif kind == 'If':
            return parse_if(term_data)
        elif kind == 'Print':
            return parse_print(term_data)

    return File(json_data['name'], parse_term(json_data['expression']), parse_location(json_data['location']))

def evaluate_term(term, env):
    if isinstance(term, Var):
        if term.text in env:
            return env[term.text]
        elif term.text in term.location.filename:
            return term
        else:
            raise KeyError(f'Variable not defined: {term.text}')
    elif isinstance(term, Function):
        return term
    elif isinstance(term, Call):
        function = evaluate_term(term.callee, env)
        arguments = [evaluate_term(arg, env) for arg in term.arguments]
        return evaluate_function_call(function, arguments, env)
    elif isinstance(term, Let):
        new_env = env.copy()
        new_env[term.name.text] = evaluate_term(term.value, env)
        return evaluate_term(term.next_term, new_env)
    elif isinstance(term, Str):
        return term.value
    elif isinstance(term, Int):
        value = term.value
        return int(value)
    elif isinstance(term, Binary):
        lhs = evaluate_term(term.lhs, env)
        rhs = evaluate_term(term.rhs, env)
        return evaluate_binary_operation(lhs, term.op, rhs)
    elif isinstance(term, Tuple):
        first = evaluate_term(term.first, env)
        second = evaluate_term(term.second, env)
        return (first, second)
    elif isinstance(term, First):
        tuple_value = evaluate_term(term.value, env)
        return tuple_value[0]
    elif isinstance(term, Second):
        tuple_value = evaluate_term(term.value, env)
        return tuple_value[1]
    elif isinstance(term, Bool):
        return term.value
    elif isinstance(term, If):
        condition = evaluate_term(term.condition, env)
        if condition:
            return evaluate_term(term.then, env)
        else:
            return evaluate_term(term.otherwise, env)
    elif isinstance(term, Print):
        value = evaluate_term(term.value, env)
        print_value(value)

        if not cache.is_empty():
            cache.clear()

        return value

def evaluate_function_call(function, arguments, env):
    cache_key = (function, tuple(arguments))

    if cache_key in cache.cache:
        return cache.get(cache_key)

    new_env = env.copy()
    for parameter, argument in zip(function.parameters, arguments):
        new_env[parameter.text] = argument
    new_env.update(function.closure_env)
    result = evaluate_term(function.value, new_env)

    cache.set(cache_key, result)

    return result

def evaluate_binary_operation(lhs, op, rhs):
    if op.kind == 'Add':
        if isinstance(lhs, str) and (isinstance(rhs, int) or isinstance(rhs, float)):
            return lhs + str(int(rhs)) if isinstance(rhs, float) and rhs.is_integer() else lhs + str(rhs)
        elif (isinstance(lhs, int) or isinstance(lhs, float)) and isinstance(rhs, str):
            return str(int(lhs)) + rhs if isinstance(lhs, float) and lhs.is_integer() else str(lhs) + rhs
        elif isinstance(lhs, str) and isinstance(rhs, str):
            return lhs + rhs
        elif isinstance(lhs, int) and isinstance(rhs, int):
            result = lhs + rhs
            if result > 2**31 - 1 or result < -2**31:
                raise OverflowError("Overflow: integers exceed 32-bit")
            return result
        elif isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        else:
            return lhs + rhs
    elif op.kind == 'Sub':
        result = lhs - rhs
        if isinstance(lhs, int) and isinstance(rhs, int):
            if np.int32(result) != result:
                raise OverflowError("Overflow: integers exceed 32-bit")
        return result
    elif op.kind == 'Mul':
        result = lhs * rhs
        if isinstance(lhs, int) and isinstance(rhs, int):
            if np.int32(result) != result:
                raise OverflowError("Overflow: integers exceed 32-bit")
        return result
    elif op.kind == 'Div':
        if rhs == 0:
            raise ZeroDivisionError("Division by zero")

        return lhs // rhs if isinstance(lhs, int) and isinstance(rhs, int) else lhs / rhs
    elif op.kind == 'Rem':
        if rhs == 0:
            raise ZeroDivisionError("Division by zero")
        return lhs % rhs
    elif op.kind == 'Eq':
        return lhs == rhs
    elif op.kind == 'Neq':
        return lhs != rhs
    elif op.kind == 'Lt':
        return lhs < rhs
    elif op.kind == 'Gt':
        return lhs > rhs
    elif op.kind == 'Lte':
        return lhs <= rhs
    elif op.kind == 'Gte':
        return lhs >= rhs
    elif op.kind == 'And':
        return lhs and rhs
    elif op.kind == 'Or':
        return lhs or rhs

def print_value(value):
    if isinstance(value, str):
        print(value, end='\n')
    elif isinstance(value, int):
        print(value, end='\n')
    elif isinstance(value, bool):
        print(value, end='\n')
    elif isinstance(value, tuple):
        print(f'({value[0]}, {value[1]})', end='\n')
    elif isinstance(value, Function):
        print('<#closure>', end='\n')

def trampoline(term, env):
    while True:
        while isinstance(term, Call):
            function = evaluate_term(term.callee, env)
            arguments = [evaluate_term(arg, env) for arg in term.arguments]

            if isinstance(function, Function):
                new_env = env.copy()
                for parameter, argument in zip(function.parameters, arguments):
                    new_env[parameter.text] = argument
                new_env.update(function.closure_env)
                term = function.value
                env = new_env
            else:
                term = evaluate_function_call(function, arguments, env)
        
        if isinstance(term, Var):
            if term.text in env:
                return env[term.text]
            elif term.text in term.location.filename:
                return term
            else:
                raise KeyError(f'Variável não definida: {term.text}')
        else:
            return term

def main():
    json_data = load_json_file('/app/var/rinha/source.rinha.json')
    ast = parse_json_to_ast(json_data)
    env = {}
    try:
        result = trampoline(ast.expression, env)
        evaluate_term(result, env)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
