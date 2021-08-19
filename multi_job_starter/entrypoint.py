#!/usr/bin/env python
"""
This is an entrypoint for multi stater app.
The goal of the app is to run asynchronously multi target scopes.
"""
import asyncio
import logging
import pathlib
from time import time

from utils.config import Config
from utils.helpers import ScriptDefinition, ArgDefinition
from utils.processes_runner import ProcessesRunner

script_definition = ScriptDefinition(
    args_definition_list=[
        ArgDefinition(short_arg='-c', full_arg='--command', name='command to run with', type=str),
        ArgDefinition(short_arg='-f', full_arg='--file-input', name='input file with targets', type=pathlib.Path),
        ArgDefinition(short_arg='-r', full_arg='--file-output', name='output file with results', type=pathlib.Path),
        ArgDefinition(short_arg='-ci', full_arg='--concurrent-instances',
                      name='number of concurrency instances', type=int),
    ],
)


async def main() -> None:
    """
    Entrypoint into the application.
    :return: None
    """
    await ProcessesRunner.run_from_cmd(script_definition=script_definition)


if __name__ == '__main__':
    try:
        start_time = time()
        asyncio.run(main(), debug=Config.DEFAULT_DEBUGGING)
        logging.log(logging.DEBUG, f'Time consumption: {time() - start_time: 0.3f}s')
    except Exception as error:
        logging.exception(f'Failed with: {error}')
