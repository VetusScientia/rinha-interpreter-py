from rinha import RinhaError, format_output

def interpret(node, environment):
    if isinstance(node, dict):
        kind = node.get("kind")
        if kind == "Int":
            return node.get("value", 0)
        elif kind == "Str":
            return node["value"]
        elif kind == "Bool":
            return node["value"]
        elif kind == "Binary":
            lhs = interpret(node.get("lhs", node), environment)
            rhs = interpret(node.get("rhs", node), environment)
            op = node["op"]
            if op == "Add" and (isinstance(lhs, str) or isinstance(rhs, str)):
                return str(lhs) + str(rhs)
            operators = {
                "Add": lhs + rhs,
                "Sub": lhs - rhs,
                "Mul": lhs * rhs,
                "Div": lhs // rhs if rhs != 0 else None,  
                "Rem": lhs % rhs if rhs != 0 else None,  
                "Eq": lhs == rhs,
                "Neq": lhs != rhs,
                "Lt": lhs < rhs,
                "Gt": lhs > rhs,
                "Lte": lhs <= rhs,
                "Gte": lhs >= rhs,
                "And": lhs and rhs,
                "Or": lhs or rhs
            }
            if op == "Div" and rhs == 0:
                raise RinhaError("Division by zero")
            return operators[op]
        elif kind == "Let":
            name = node["name"]["text"]
            value = interpret(node["value"], environment)
            new_environment = environment.copy()  
            new_environment[name] = value
            return interpret(node.get("next", node), new_environment)
        elif kind == "If":
            condition = interpret(node["condition"], environment)
            return interpret(node["then"] if condition else node["otherwise"], environment)
        elif node["kind"] == "Print":
            value = interpret(node["value"], environment)
            print(f"Output: {format_output(value)}")
            return "Program finished"
        elif kind == "Function":
            return node
        elif kind == "Call":
            callee = interpret(node["callee"], environment)
            args = [interpret(arg, environment) for arg in node["arguments"]]
            if callee["kind"] == "Function":
                if "name" not in callee:
                    func_node = callee["value"]
                    func_environment = environment.copy()
                    for param, arg in zip(callee["parameters"], args):
                        func_environment[param["text"]] = arg
                    return interpret(func_node, func_environment)
        elif kind in ("First", "Second"):
            tuple_value = interpret(node["value"], environment)
            if isinstance(tuple_value, tuple):
                return tuple_value[0] if kind == "First" else tuple_value[1]
            else:
                raise RinhaError(f"Expected a tuple, got {type(tuple_value).__name__}")
        elif kind == "Tuple":
            first = interpret(node["first"], environment)
            second = interpret(node["second"], environment)
            return (first, second)
        elif kind == "Var":
            var_name = node["text"]
            return environment.get(var_name, RinhaError(f"Variable '{var_name}' not defined"))
        elif kind == "Parameter":
            return node

    return node
