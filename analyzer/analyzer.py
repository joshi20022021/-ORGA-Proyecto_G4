from .parser.parser import parser
from typing import List

from .printjob import PrintJob


"""
    @author: sebas-v-c
    @program: an analyzer for an input file
"""


def analyze_file(file_path: str) -> List[PrintJob]:
    """File analyzer for the input data
    Args:
        file_path (str): The path to the input file

    Returns:
        List[PrintJob]: returns a list of the declared print jobs in the input file

    """
    data: List[PrintJob] = []
    with open(file_path, "r") as file:
        input_text = file.read()
        data = parser.parse(input_text)

    for d in data:
        d.order_instructions()

    return data
