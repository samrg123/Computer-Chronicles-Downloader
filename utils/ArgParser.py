from argparse import ArgumentParser
from dataclasses import dataclass, fields
from typing import Type, TypeVar


@dataclass(kw_only=True)
class ArgParseArg:
    help    : str  = ""
    metavar : str  = ""
    default : str  = "",
    type    : Type = str,
    action  : str  = "store"
    required: bool = False

@dataclass(kw_only=True)
class Arg(ArgParseArg):
    longName: str = ""
    value   : str = None

    def formattedHelpStr(self) -> str:        
        
        helpStr = self.help.strip()
        
        if self.default is not None:
            metavarStr = f"[{self.metavar.strip()}]" if self.metavar else ""
            helpStr+= f" Default {metavarStr} = '{self.default}'"

        return helpStr
    
    def __str__(self) -> str:
        return f"{self.__dict__}"

class Args:
    def ArgDict(self) -> dict[str, Arg]:

        argDict = {}
        for attribName in dir(self):
            attrib = getattr(self, attribName)

            if isinstance(attrib, Arg):        
                argDict[attribName] = attrib

        return argDict

    def __str__(self) -> str:
        result = "["
        for name, arg in self.ArgDict().items():
            result+= f"\n\t {name} = {str(arg)}"
        result+= "]"

        return result
    
ArgsT = TypeVar("ArgsT", bound=Args)
class ArgParser(ArgumentParser):

    def Parse(self, args: ArgsT) -> ArgsT:

        argDict = args.ArgDict()
        kwKeys = [field.name for field in fields(ArgParseArg)]

        # invoke self.add_argument for each of our Arg fields
        for name, arg in argDict.items():

            argVars = vars(arg)
            
            # Note: Dataclass packs the default type into a 1-element tuple (No idea why)
            #       so we dereference it here
            argType = arg.type
            if isinstance(argType, tuple):
                argType = argType[0]

            kwDict = { key: argVars[key] for key in kwKeys } | {
                "type": argType, 
                "help": arg.formattedHelpStr(),
                "dest": name
            }

            # Remove unsupported arguments for store_true action
            if kwDict["action"] == "store_true":
                kwDict.pop("metavar")
                kwDict.pop("type")

            self.add_argument(arg.longName, **kwDict)

        parsedResults = self.parse_args()

        # populate arg values
        for name, arg in argDict.items():
            arg.value = getattr(parsedResults, name)

        return args