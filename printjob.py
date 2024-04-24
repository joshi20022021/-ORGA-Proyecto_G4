#!/usr/bin/env python3


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
        self.instructions: list[Instruction] = []

    def __str__(self):
        inst_data = ""
        for inst in self.instructions:
            inst_data = str(inst) + "\n"

        return f"Name: {self.name}\nInstructions:\n{inst_data}"
