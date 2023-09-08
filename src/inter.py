import json
import argparse

def interpret(node, environment):
    try:
        if node["kind"] == "Int":
            return node["value"]
        elif node["kind"] == "Str":
            return node["value"]
        elif node["kind"] == "Bool":
            return node["value"]
        elif node["kind"] == "Binary":
            lhs = interpret(node["lhs"], environment)
            rhs = interpret(node["rhs"], environment)
            op = node["op"]
            if op == "Add":
                return lhs + rhs
            elif op == "Sub":
                return lhs - rhs
            elif op == "Mul":
                return lhs * rhs
            elif op == "Div":
                if rhs == 0:
                    raise ValueError("Division by zero")
                return lhs / rhs
            elif op == "Rem":
                return lhs % rhs
            elif op == "Eq":
                return lhs == rhs
            elif op == "Neq":
                return lhs != rhs
            elif op == "Lt":
                return lhs < rhs
            elif op == "Gt":
                return lhs > rhs
            elif op == "Lte":
                return lhs <= rhs
            elif op == "Gte":
                return lhs >= rhs
            elif op == "And":
                return lhs and rhs
            elif op == "Or":
                return lhs or rhs
        elif node["kind"] == "Let":
            name = node["name"]["text"]
            value = interpret(node["value"], environment)
            new_environment = {**environment, name: value}
            return interpret(node["next"], new_environment)
        elif node["kind"] == "If":
            condition = interpret(node["condition"], environment)
            if condition:
                return interpret(node["then"], environment)
            else:
                return interpret(node["otherwise"], environment)
        elif node["kind"] == "Print":
            term = interpret(node["value"], environment)
            print(term)
            return "Finished program"
        elif node["kind"] == "Function":
            return node
        elif node["kind"] == "Call":
            callee = interpret(node["callee"], environment)
            args = [interpret(arg, environment) for arg in node["arguments"]]
            new_environment = {**environment}
            for param, arg in zip(callee["parameters"], args):
                new_environment[param["text"]] = arg
            return interpret(callee["value"], new_environment)
        elif node["kind"] == "First":
            tuple_value = interpret(node["value"], environment)
            if isinstance(tuple_value, tuple):
                return tuple_value[0]
            else:
                raise TypeError(f"Expected a tuple, got {type(tuple_value).__name__}")
        elif node["kind"] == "Second":
            tuple_value = interpret(node["value"], environment)
            if isinstance(tuple_value, tuple):
                return tuple_value[1]
            else:
                raise TypeError(f"Expected a tuple, got {type(tuple_value).__name__}")
        elif node["kind"] == "Tuple":
            first = interpret(node["first"], environment)
            second = interpret(node["second"], environment)
            return (first, second)
        elif node["kind"] == "Var":
            var_name = node["text"]
            if var_name in environment:
                return environment[var_name]
            else:
                raise NameError(f"Variable '{var_name}' not defined")
        elif node["kind"] == "Parameter":
            return node
        else:
            raise ValueError(f"Invalid node kind: {node['kind']}")
    except Exception as e:
        print(f"Erro: {e}")

def load_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpretador para a linguagem Rinha')
    parser.add_argument('-s', '--start', metavar='filename', type=str, help='Inicia a interpretação a partir de um arquivo JSON')
    parser.add_argument('-v', '--version', action='store_true', help='Exibe a versão do interpretador')

    args = parser.parse_args()

    if args.version:
        print("Rinha Interpreter v1.0")
    elif args.start:
        try:
            filename = args.start

            if not filename.endswith('.json'):
                raise ValueError("O arquivo deve ter a extensão .json")
        except Exception as e:
            print(f"Erro: {e}")
        else:
            data = load_json_file(filename)
            resultado = interpret(data["expression"], {})
            print(resultado)
    else:
        print("Utilize 'rinha -h' ou 'rinha --help' para obter ajuda.")
