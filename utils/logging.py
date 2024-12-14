import traceback
from datetime import datetime

from typing import Final
from dataclasses import dataclass, fields

@dataclass
class LogLevel:
    Error  : Final[int] = 0
    Default: Final[int] = 1
    Verbose: Final[int] = 2

    @staticmethod
    def getMapping() -> dict[str, int]:
        """Returns a dict LogLevel fields to values sorted in ascending value order"""
        mapping = {field.name: field.default for field in fields(LogLevel)}
        return dict(sorted(mapping.items(), key=lambda item: item[1]))

gLogLevel:int = LogLevel.Default

def setLogLevel(level:int) -> int:
    """Sets gLogLevel to `level` and returns the previously set level"""

    global gLogLevel
    oldLevel = gLogLevel
    gLogLevel = level

    log(f"Changed gLogLevel from '{oldLevel}' to '{gLogLevel}'", logLevel=LogLevel.Verbose)

    return oldLevel

def log(msg, prefix:str="MSG", logLevel:int=LogLevel.Default) -> None:

    if gLogLevel >= logLevel:

        timeStr = datetime.now().strftime("%H:%M:%S:%f") 
    
        msgStart = f"{timeStr} -- {prefix}[{logLevel}]: "
        msgBody = str(msg).replace("\n", "\n"+" "*len(msgStart))    
    
        print(msgStart + msgBody)

def panic(msg) -> None:
    log(msg, "PANIC", logLevel=LogLevel.Error)
    traceback.print_stack()
    exit(1)

def warn(msg) -> None:
    log(msg, prefix="WARN", logLevel=LogLevel.Error)

def error(msg) -> None:
    log(msg, prefix="ERROR", logLevel=LogLevel.Error)    