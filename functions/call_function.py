import sys

def call_function(function_call_part, verbose=False):
    if "--verbose" in sys.argv:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        result = function_call_part.name()
    print(f"- Calling function: {function_call_part.name}")

