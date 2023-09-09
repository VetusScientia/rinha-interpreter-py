import argparse
import resource
from rinha import RinhaError, load_json_file
from interpreter import interpret

start_time = None

def start_timer():
    global start_time
    start_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime + resource.getrusage(resource.RUSAGE_SELF).ru_stime

def end_timer():
    global start_time
    end_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime + resource.getrusage(resource.RUSAGE_SELF).ru_stime
    cpu_time = end_time - start_time
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # MB
    print(f"CPU Time: {cpu_time} seconds")
    print(f"Memory Usage: {memory_usage} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for Rinha language')
    parser.add_argument('-s', '--start', metavar='filename', type=str, help='Starts parsing from a JSON file')
    parser.add_argument('-v', '--version', action='store_true', help='Displays the interpreter version')

    args = parser.parse_args()

    if args.version:
        print("Rinha Interpreter v1.1")
    elif args.start:
        try:
            filename = args.start

            if not filename.endswith('.json'):
                raise RinhaError("The file must have the .json extension")
        except Exception as e:
            print(f"Error: {e}")
        else:
            start_timer()

            data = load_json_file(filename)
            output = interpret(data["expression"], {})
            print(output)

            end_timer()
    else:
        print("Use 'rinha -h' or 'rinha --help' to get help.")
