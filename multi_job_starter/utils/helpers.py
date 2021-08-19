"""
This module provides helpers for the app.
"""
from argparse import ArgumentParser, Namespace
from typing import NamedTuple, Optional, Type


class ArgDefinition(NamedTuple):
    """
    ArgDefinition class to work with argparse.
    """
    short_arg: str
    full_arg: str
    name: str
    type: Type


class ScriptDefinition(NamedTuple):
    """
    ScriptDefinition class to work with arguments.
    """
    args_definition_list: list[ArgDefinition]
    print_stderr: Optional[bool] = False
    library_result_file: Optional[str] = None


def create_arguments_parser(args_definition_list: list[ArgDefinition]) -> Namespace:
    """
    Here implements arguments parser for parsing user arguments to the main script file
    :param args_definition_list: List[ArgDefinition]
    :return: argparse.Namespace
    """
    # Construct the argument parser
    ap = ArgumentParser()

    # Add the arguments to the parser
    for argument in args_definition_list:
        ap.add_argument(
            argument.short_arg,
            argument.full_arg,
            required=True,
            type=argument.type,
            help=argument.name,
        )

    return ap.parse_args()
