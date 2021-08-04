import asyncio
import json
import pathlib
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from typing import Generator, Coroutine, Any

from .config import Types
from .helpers import ScriptDefinition, ArgDefinition
from .task_runner import TaskRunner


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


def get_targets_from_file(file_path: pathlib.Path) -> list[str]:
    return file_path.read_text().splitlines()


def save_results_to_file(file_path: pathlib.Path, results: str) -> None:
    file_path.write_text(results)


@dataclass
class ProcessesRunner:
    targets: list[str]
    tasks: Generator[Coroutine[Any, Any, TaskRunner], Any, None] = field(default_factory=list)

    @classmethod
    async def run_from_cmd(cls, script_definition: ScriptDefinition) -> None:
        args: Namespace = create_arguments_parser(args_definition_list=script_definition.args_definition_list)
        obj: ProcessesRunner = cls(targets=get_targets_from_file(file_path=args.file_input))
        obj._create_tasks(command=args.command, max_concurrent_instances=int(args.concurrent_instances))
        results: Types.ASYNCIO_GATHER = await obj.start_jobs()
        save_results_to_file(file_path=args.file_output, results=json.dumps([result.to_json() for result in results]))

    async def start_jobs(self) -> Types.ASYNCIO_GATHER:
        return await asyncio.gather(*self.tasks)

    def _create_tasks(self, command: str, max_concurrent_instances: int) -> None:
        semaphore: asyncio.BoundedSemaphore = asyncio.BoundedSemaphore(max_concurrent_instances)
        self.tasks = (TaskRunner.create_run_task(
            command=command, target=target, semaphore=semaphore,
        ) for target in self.targets)
