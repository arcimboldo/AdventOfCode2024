from utils import app
import re


class State:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.ptr = 0
        self.output = []

    def next(self):
        """Run the current instruction"""
        operands = {
            0: adv,
            1: bxl,
            2: bst,
            3: jnz,
            4: bxc,
            5: out,
            6: bdv,
            7: cdv,
        }
        opcode = self.program[self.ptr]
        func = operands[opcode]
        op = self.program[self.ptr + 1]

        ret = func(op, self)
        # print(
        #     f"Running function opcode {opcode} at ptr {self.ptr}: {func.__name__}({op}) -> {ret}"
        # )
        if ret is not None:
            self.ptr = ret
        else:
            self.ptr += 2


def combo(op, state):
    return {0: 0, 1: 1, 2: 2, 3: 3, 4: state.A, 5: state.B, 6: state.C}[op]


def adv(op, state):
    """The adv instruction (opcode 0) performs division. The numerator is the
    value in the A register. The denominator is found by raising 2 to the power
    of the instruction's combo operand. (So, an operand of 2 would divide A by 4
    (2^2); an operand of 5 would divide A by 2^B.) The result of the division
    operation is truncated to an integer and then written to the A register."""
    state.A = state.A // 2 ** combo(op, state)


def bxl(op, state):
    """The bxl instruction (opcode 1) calculates the bitwise XOR of register B
    and the instruction's literal operand, then stores the result in register
    B."""
    state.B = state.B ^ op


def bst(op, state):
    """The bst instruction (opcode 2) calculates the value of its combo operand
    modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to
    the B register."""
    state.B = combo(op, state) % 8


def jnz(op, state):
    """The jnz instruction (opcode 3) does nothing if the A register is 0.
    However, if the A register is not zero, it jumps by setting the instruction
    pointer to the value of its literal operand; if this instruction jumps, the
    instruction pointer is not increased by 2 after this instruction."""
    if state.A != 0:
        return op


def bxc(op, state):
    """The bxc instruction (opcode 4) calculates the bitwise XOR of register B
    and register C, then stores the result in register B. (For legacy reasons,
    this instruction reads an operand but ignores it.)"""
    state.B = state.B ^ state.C


def out(op, state):
    """The out instruction (opcode 5) calculates the value of its combo operand
    modulo 8, then outputs that value. (If a program outputs multiple values,
    they are separated by commas.)"""
    state.output.append(str(combo(op, state) % 8))


def bdv(op, state):
    """The bdv instruction (opcode 6) works exactly like the adv instruction
    except that the result is stored in the B register. (The numerator is still
    read from the A register.)"""
    state.B = state.A // 2 ** combo(op, state)


def cdv(op, state):
    """The cdv instruction (opcode 7) works exactly like the adv instruction
    except that the result is stored in the C register. (The numerator is still
    read from the A register.)"""
    state.C = state.A // 2 ** combo(op, state)


def parse(txt):
    lines = [line.split(":")[-1] for line in txt.splitlines() if ":" in line]
    A = int(lines[0])
    B = int(lines[1])
    C = int(lines[2])
    program = list(map(int, lines[3].split(",")))
    return A, B, C, program


class App(app.App):
    def part_one(self):
        state = State(*parse(self.data))

        while state.ptr < len(state.program):
            state.next()
        output = str.join(",", state.output)
        print(f'Output: {output}')
        return output

    def part_two(self):
        pass


myapp = App(
    """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
)

myapp.test_one('4,6,3,5,6,3,5,2,1,0', '5,0,3,5,7,6,1,5,4')

myapp.run()
