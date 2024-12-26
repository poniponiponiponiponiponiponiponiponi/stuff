import subprocess
import string

def execute_program(program, input_string):
    try:
        process = subprocess.Popen(
            program,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=input_string)
        
        return_code = process.returncode
        return stdout, stderr, return_code

    except FileNotFoundError:
        return None, f"Error: Program '{program[0]}' not found.", -1
    except Exception as e:
        return None, f"An error occurred: {e}", -1


def execute(inp):
    program_to_execute = ["valgrind", "--tool=callgrind", "./chal2"]
    stdout, stderr, return_code = execute_program(program_to_execute, inp)
    return int(stderr.split("Collected : ")[1].split('\n')[0])
for c in string.printable:
    print(c, end=' ')
    print(execute("01" +c + "$"))
