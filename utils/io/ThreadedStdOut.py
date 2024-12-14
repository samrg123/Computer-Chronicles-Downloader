import os
import sys
import io
import threading

from collections.abc import Iterable

class ThreadedStdOut:

    _globalBuffers: dict[int, io.StringIO] = {}
    _globalBuffersLock = threading.Lock()

    class BufferReference():
        def __enter__(self) -> io.StringIO:
            ThreadedStdOut._globalBuffersLock.acquire()
            
            threadId = threading.get_ident()
            if threadId in ThreadedStdOut._globalBuffers:
                return ThreadedStdOut._globalBuffers[threadId]

            buffer = io.StringIO()
            ThreadedStdOut._globalBuffers[threadId] = buffer
            return buffer

        def __exit__(self, type, value, traceback) -> None:
            ThreadedStdOut._globalBuffersLock.release()


    def write(self, s: str) -> int:
        with ThreadedStdOut.BufferReference() as buffer:
            result = buffer.write(s)
            self._update()
            return result
    
    def writelines(self, lines: Iterable[str]) -> None:
        with ThreadedStdOut.BufferReference() as buffer:
            result = buffer.writelines(lines)
            self._update()
            return result

    def read(self, size: int) -> str:
        with ThreadedStdOut.BufferReference() as buffer:
            return buffer.read(size)

    def readline(self, size: int = -1) -> str:
        with ThreadedStdOut.BufferReference() as buffer:
            return buffer.readline(size)

    def readlines(self, hint: int = -1) -> list[str]:
        with ThreadedStdOut.BufferReference() as buffer:
            return buffer.readlines(hint)

    def seek(self, cookie: int, whence: int = 0) -> int:
        with ThreadedStdOut.BufferReference() as buffer:
            return buffer.seek(cookie, whence)

    def __init__(self, header:str = "", stdout = sys.stdout) -> None:
        self.header = header
        self.stdout = stdout
        self._update()

    def _update(self) -> None:
        numTermCols, numTermLines = os.get_terminal_size()

        # Go home and clear screen
        combinedBuffer = f"\x1B[H\x1B[J{self.header}\n"

        for threadId, buffer in ThreadedStdOut._globalBuffers.items():
            
            bufferContent = buffer.getvalue()
            bufferContentLen = len(bufferContent)

            # grab the last non-blank line to print
            prevNewLineIndex = bufferContentLen
            while True:
                newLineIndex = bufferContent.rfind("\n", 0, prevNewLineIndex)

                lineIndex = newLineIndex + 1
                strippedLine = bufferContent[lineIndex:prevNewLineIndex].strip()

                if lineIndex == 0 or len(strippedLine) > 0:
                    break

                prevNewLineIndex = newLineIndex
                
            # truncate buffer to last line to prevent memory overflow
            buffer.seek(0)
            buffer.truncate(0)
            buffer.write(bufferContent[lineIndex:])

            prefix = f"[{threadId:06}] - "
            combinedBuffer+= f"{prefix}{strippedLine}"[:numTermCols] + "\n"

        self.stdout.write(combinedBuffer)