import json

class RinhaError(Exception):
    def __init__(self, message):
        super().__init__(message)

def format_output(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, int) or isinstance(value, float):
        return str(value)
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif callable(value):
        return "<#closure>"
    elif isinstance(value, tuple):
        return f"({format_output(value[0])}, {format_output(value[1])})"
    elif isinstance(value, dict):
        return json.dumps(value)
    else:
        raise RinhaError(f"Invalid output format for value: {value}")

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
