from parser import parser
from typing import List, Dict

"""
    @author: sebas-v-c
    @program: an analyzer for an input file
"""


def analyze_file(file_path: str):
    """File analyzer for the input data
    Args:
        file_path (str): The path to the input file

    Returns:
        List[]

    """
    with open(file_path, "r") as file:
        input_text = file.read()
        return parser.parse(input_text)


data = analyze_file(
    "/home/zibas/Documents/USAC/SEMESTRE-7/IO1/proyecto-final/-ORGA-Proyecto_G4/test_file.txt"
)


for d in data:
    print(d)
