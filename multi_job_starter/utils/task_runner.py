import asyncio
from asyncio import BoundedSemaphore
from asyncio.subprocess import Process
from dataclasses import dataclass, field
from shlex import quote as shlex_quot

from .config import Config


@dataclass
class TaskRunner:
    _command: str
    _target: str
    _semaphore: BoundedSemaphore = field(metadata={'include_in_dict': False})
    _raw_result: str = field(default=None)
    _status_code: int = field(default=None)
    _error_message: str = field(default=None)
    _max_rerun_tries_left: int = field(default=Config.ATTEMPTS_TO_RETRY)

    @classmethod
    async def create_run_task(cls, command: str, target: str, semaphore: BoundedSemaphore) -> 'TaskRunner':
        # noinspection StrFormat
        obj: TaskRunner = cls(_command=command.format(shlex_quot(target)), _target=target, _semaphore=semaphore)
        return await obj.start_task()

    async def start_task(self) -> 'TaskRunner':
        return await self._run_task()

    async def _run_task(self) -> 'TaskRunner':
        async with self.semaphore:
            process: Process = await asyncio.create_subprocess_shell(
                self.command,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            await self._receive_result(process=process)
            return self

    async def _receive_result(self, process: Process) -> None:
        stdout, stderr = await process.communicate()
        self._raw_result: str = stdout.decode().strip()
        self._error_message: str = stderr.decode().strip()
        self._status_code: int = process.returncode

    async def rerun_task(self) -> 'TaskRunner':
        if not self.max_rerun_tries:
            return self
        self._max_rerun_tries_lower()
        return await self._run_task()

    def to_json(self) -> dict[str, str]:
        return {key: value for key, value in self.__dict__.items() if key not in ['_semaphore']}

    def _max_rerun_tries_lower(self) -> None:
        self._max_rerun_tries_left -= 1

    @property
    def command(self) -> str:
        return self._command

    @property
    def target(self) -> str:
        return self._target

    @property
    def semaphore(self) -> BoundedSemaphore:
        return self._semaphore

    @property
    def raw_result(self) -> str:
        return self._raw_result

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def max_rerun_tries(self) -> int:
        return self._max_rerun_tries_left

    @property
    def error_message(self) -> str:
        return self._error_message
