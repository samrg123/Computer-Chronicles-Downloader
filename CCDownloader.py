import os
import re
from utils.ArgParser import *
from utils.logging import *

from utils.FileDownloader import FileDownloader, DownloadFile

def GetInfoStr(header:str, info:list) -> str:
    infoStr = f"===== {header} =====\n"

    if isinstance(info, dict):
        
        sortedKeys = sorted(info.keys())

        keyStrs = [ f"   {key}" for key in sortedKeys ]
        
        maxKeyStrLen = len(max(keyStrs, key=len))
        maxIndentStr = ' ' * maxKeyStrLen

        for i,key in enumerate(sortedKeys):
            val    = info[key] 
            keyStr = keyStrs[i]
            
            valStr = maxIndentStr[len(keyStr):] + f" = {f',\n   {maxIndentStr}'.join(val) if isinstance(val, list) else val}"

            infoStr+= f"{keyStr}{valStr}\n"

        infoStr+= f"Total Items: {len(info)}\n"

    elif isinstance(info, list) or isinstance(info, set):
        infoStr+= f"   {f',\n   '.join(sorted(info))}\nTotal Items: {len(info)}\n"

    else:
        infoStr += f"{info}\n"

    return infoStr + f"=====\n"


gListedInfo = False
def ListInfo(header:str, infos:list) -> None:
    global gListedInfo 

    print(GetInfoStr(header, infos))
    gListedInfo = True

def main():

    # scan the save dir to save the files to and a

    class MainArgs(Args):        
        dir          = Arg(longName="--dir",          metavar="str",  type=str, default="./Computer Chronicles", help=f"Specifies the directory to download to.")
        file         = Arg(longName="--file",         metavar="str",  type=str, default="./files.xml",           help=f"Specifies the download xml file to parse.")
        listAll      = Arg(longName="--listAll",      action="store_true",      default=False,                   help=f"Lists all information and exits.")
        listFile     = Arg(longName="--listFile",     action="store_true",      default=False,                   help=f"Lists the files in `{file.longName}` and exits.")
        listDir      = Arg(longName="--listDir",      action="store_true",      default=False,                   help=f"Lists the files in `{dir.longName}` and exits.")
        listDownload = Arg(longName="--listDownload", action="store_true",      default=False,                   help=f"Lists the non existing `{file.longName}` files in `{dir.longName}` that will be downloaded and exits.")
        listRepeat   = Arg(longName="--listRepeat",   action="store_true",      default=False,                   help=f"Lists the 'REPEAT' files in `{file.longName}` that will be ignored and exits.")
        listLinks    = Arg(longName="--listLinks",    action="store_true",      default=False,                   help=f"Lists the 'REPEAT' files in `{file.longName}` as linux `ln` commands to original files and exits.")
        threads      = Arg(longName="--threads",      metavar="int",  type=int, default=max(5, os.cpu_count()),  help=f"Specifies the number of threads to use while downloading.")
        verbose      = Arg(longName="--verbose",      metavar="int",  type=int, default=LogLevel.Default,        help=f"Specifies the verbose log level. Larger values enable more verbose output. Log Levels: {LogLevel.getMapping()}")

    argParser = ArgParser(
        description = "A lightweight python utility for downloading recorded computer chronicle episodes"
    )

    args = argParser.Parse(MainArgs())

    setLogLevel(args.verbose.value)

    argStr = "\n".join([f"\t{name} [{type(arg.value)}] = '{arg.value}'" for name, arg in args.ArgDict().items()])
    log(f"Using args: {{\n{argStr}\n}}", logLevel=LogLevel.Verbose)


    filePath = args.file.value
    dirPath  = args.dir.value

    parsedFile = FileDownloader.ParseFile(filePath)
    dirFiles   = FileDownloader.ParseDir(dirPath)

    relativeDirFiles = set([os.path.relpath(path, dirPath) for path in dirFiles])
    repeatFiles = { key:val for key,val in parsedFile.items() if " REPEAT [" in key } 

    downloadFile     = DownloadFile({key: parsedFile[key] for key in sorted(parsedFile.keys() - relativeDirFiles - repeatFiles.keys())})

    # parse list args
    listAll = args.listAll.value
    if(listAll or args.listFile.value):
        ListInfo(f"Files in '{filePath}'", parsedFile)

    if(listAll or args.listDir.value):
        ListInfo(f"Files in '{dirPath}'", relativeDirFiles)

    if(listAll or args.listDownload.value):
        ListInfo("Files to Download", downloadFile)

    if(listAll or args.listRepeat.value):
        ListInfo("Repeat Files", repeatFiles)

    if(listAll or args.listLinks.value):
        
        linkFiles = []
        for repeatName in sorted(repeatFiles.keys()):
            
            matches = re.match(r"^.* REPEAT \[(.*)\]\.(.*)$", repeatName)
            if matches == None or len(matches.groups()) != 2:
                warn(f"Failed to parse original name in repeat file: '{repeatName}' - ignoring")
                continue 

            title, extension =  matches.group(1, 2)
            searchName = f" - {title}.{extension}" 

            linkName:str|None = None
            for downloadName in sorted(downloadFile.keys()):

                if searchName.lower() in downloadName.lower():
                    if linkName != None:
                        warn(f"repeat file '{repeatName}' matches original file '{linkName}' and '{downloadName}' - using first sorted match") 
                        continue

                    linkName = downloadName

            if linkName == None:
                warn(f"Failed to find link to '{repeatName}'")
                continue

            linkFiles.append(f'ln "{linkName.replace("\\","/")}" "{repeatName.replace("\\","/")}"')

        ListInfo("Files to Link", linkFiles)

    if gListedInfo:
        return

    # download the files
    log(GetInfoStr("Downloading Files", downloadFile))
    FileDownloader.Download(downloadFile=downloadFile, dir=dirPath, numThreads=args.threads.value)


if __name__ == "__main__":
    main()
