from typing import NamedTuple, Optional, Type


class ArgDefinition(NamedTuple):
    short_arg: str
    full_arg: str
    name: str
    type: Type


class ScriptDefinition(NamedTuple):
    args_definition_list: list[ArgDefinition]
    print_stderr: Optional[bool] = False
    library_result_file: Optional[str] = None
