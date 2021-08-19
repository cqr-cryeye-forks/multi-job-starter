"""
File module to work with files.
It can read and write to files with predefined file names.
"""
import json
from dataclasses import dataclass
from typing import Generator


@dataclass
class FileModule:
    """
    File module to work with files.
    """
    input_file_name: str
    result_file_name: str

    def read_input_file(self) -> Generator:
        """
        Method to read input file.
        :return: Generator reads row by row.
        """
        yield from open(self.input_file_name)

    def write_result_file(self, results: list[dict[str, str]]) -> None:
        """
        Method to write results in a file.
        Converts into string with json.dumps().
        :param results: list[dict[str, str]]
        :return: None
        """
        with open(self.result_file_name, 'w') as file:
            file.write(json.dumps(results))
