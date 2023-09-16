import ujson

class RinhaError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Closure:
    def __init__(self, func_node, environment):
        self.func_node = func_node
        self.environment = environment

    def __str__(self):
        return "<#closure>"


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
