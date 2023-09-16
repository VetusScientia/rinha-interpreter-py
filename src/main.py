import argparse
from interpreter import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for Rinha language')
    parser.add_argument('-s', '--start', metavar='filename', type=str, help='Starts parsing from a JSON file')
    parser.add_argument('-v', '--version', action='store_true', help='Displays the interpreter version')

    args = parser.parse_args()

    if args.version:
        print("Rinha Interpreter v1.1.5")
    elif args.start:
        try:
            filename = args.start

            if not filename.endswith('.json'):
                raise RinhaError("The file must have the .json extension")
        except Exception as e:
            print(f"Error: {e}")
        else:
            data = load_json_file(filename)
            output = interpret(data["expression"], {})
            print(output)
    else:
        print("Use 'rinha -h' or 'rinha --help' to get help.")

