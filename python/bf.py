import sys
from typing import ClassVar


class BrainfuckInterpreter:
    VALID_TOKENS: ClassVar[set[str]] = set("><+-.,[]")
    TAPE_SIZE: ClassVar[int] = 30_000

    @staticmethod
    def run(program: str):
        code = [c for c in program if c in BrainfuckInterpreter.VALID_TOKENS]

        stk = []
        jmp = {}

        for i, c in enumerate(code):
            match c:
                case "[":
                    stk.append(i)
                case "]":
                    j = stk.pop()
                    jmp[i], jmp[j] = j, i

        tape = [0] * BrainfuckInterpreter.TAPE_SIZE
        ptr = 0
        pc = 0

        while pc < len(code):
            match code[pc]:
                case ">":
                    ptr += 1
                    if ptr >= BrainfuckInterpreter.TAPE_SIZE:
                        sys.exit("error: Tape pointer out of bounds")
                case "<":
                    ptr -= 1
                    if ptr < 0:
                        sys.exit("error: Tape pointer out of bounds")
                case "+":
                    tape[ptr] = (tape[ptr] + 1) & 0xFF
                case "-":
                    tape[ptr] = (tape[ptr] - 1) & 0xFF
                case ".":
                    sys.stdout.write(chr(tape[ptr]))
                case ",":
                    ch = sys.stdin.read(1)
                    tape[ptr] = ord(ch) if ch else 0
                case "[":
                    if tape[ptr] == 0:
                        pc = jmp[pc]
                case "]":
                    if tape[ptr] != 0:
                        pc = jmp[pc]
            pc += 1


if __name__ == "__main__":
    fp = sys.argv[1]
    with open(fp, "r") as f:
        BrainfuckInterpreter.run(f.read())
