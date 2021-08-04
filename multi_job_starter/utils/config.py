"""
Config and Typing module.
Config is for carrying configuration constants.
Types is for carrying complex types.
"""
import os
from types import TracebackType
from typing import Type, Union, Optional, Any


class Config:
    """Config class with bunch of constants"""
    ATTEMPTS_TO_RETRY: int = os.environ.get('LIMIT_OF_ATTEMPTS_TO_RETRY', 5)
    DEFAULT_DEBUGGING: bool = os.environ.get('DEFAULT_DEBUGGING', False)


class Types:
    """Types with bunch of complex types"""
    EXC_INFO: Type = Union[tuple[type, BaseException, Optional[TracebackType]], tuple[None, None, None]]
    ASYNCIO_GATHER: Type = tuple[
        Union[BaseException, Any], Union[BaseException, Any],
        Union[BaseException, Any], Union[BaseException, Any], Union[BaseException, Any]
    ]
