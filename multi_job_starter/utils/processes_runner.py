"""
Module with ProcessesRunner.
Class is responsible for creating and running jobs.
"""
import asyncio
from argparse import Namespace
from dataclasses import dataclass, field
from typing import Generator, Coroutine, Any

from .config import Types
from .file_module import FileModule
from .helpers import ScriptDefinition, create_arguments_parser
from .task_runner import TaskRunner


@dataclass
class ProcessesRunner:
    """
    Class to create and start processes.
    """
    targets: Generator[str, Any, None]
    tasks: Generator[Coroutine[Any, Any, TaskRunner], Any, None] = field(default_factory=list)

    @classmethod
    async def run_from_cmd(cls, script_definition: ScriptDefinition) -> None:
        """
        Method to create ProcessesRunner object, tasks, start jobs and save results to a file.
        :param script_definition: ScriptDefinition
        :return: None
        """
        args: Namespace = create_arguments_parser(args_definition_list=script_definition.args_definition_list)
        file_module: FileModule = FileModule(input_file_name=args.file_input, result_file_name=args.file_output)
        obj: ProcessesRunner = cls(targets=file_module.read_input_file())
        obj._create_tasks(command=args.command, max_concurrent_instances=int(args.concurrent_instances))
        results: Types.ASYNCIO_GATHER = await obj.start_jobs()
        file_module.write_result_file(results=[result.to_json() for result in results])

    async def start_jobs(self) -> Types.ASYNCIO_GATHER:
        """
        Method to start jobs with asyncio.
        :return: Types.ASYNCIO_GATHER results from asyncio asynchronously run jobs..
        """
        return await asyncio.gather(*self.tasks)

    def _create_tasks(self, command: str, max_concurrent_instances: int) -> None:
        """
        Method which creates jobs with asyncio.BoundedSemaphore from targets.
        :param command: str command to run.
        :param max_concurrent_instances: int maximum number of concurrent instances to run jobs.
        :return: None
        """
        semaphore: asyncio.BoundedSemaphore = asyncio.BoundedSemaphore(max_concurrent_instances)
        self.tasks = (TaskRunner.create_run_task(
            command=command, target=target.strip(), semaphore=semaphore,
        ) for target in self.targets)
