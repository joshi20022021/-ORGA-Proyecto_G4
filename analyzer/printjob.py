#!/usr/bin/env python3


table = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]


class Instruction:
    def __init__(self, shape: str, row: int, column: int, color: str):
        self.shape = shape
        self.row = row
        self.column = column
        self.color = color

    def __str__(self):
        return f"Instruction(shape={self.shape}, row={self.row}, column={self.column}, color={self.color})"


class PrintJob:
    def __init__(self, name: str):
        self.name = name
        self._instructions: list[Instruction] = []

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, instructions: list[Instruction]):

        coordenates = [(x.row, x.column) for x in instructions]
        for coord in table:
            if not coord in coordenates:
                instructions.append(Instruction(" ", coord[0], coord[1], " "))

        self._instructions = instructions

    def order_instructions(self):
        sorting_key = lambda move: (move.row * 3) + move.column

        sorted_instructions = sorted(self._instructions, key=sorting_key)
        self._instructions = sorted_instructions

    def __str__(self):
        inst_data = ""
        for inst in self._instructions:
            inst_data += "\t\t" + str(inst) + ",\n"

        return f"PrintJob(\n\tname={self.name},\n\tinstructions=[\n{inst_data}\t]\n)"
