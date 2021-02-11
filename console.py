import colored
import cursor
import win32console
from pywintypes import error as winerror
from dill.source import getsource



class Cursor:

    class Coords:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return f"x: {self.x} y: {self.y}"

    @staticmethod
    def show():
        cursor.show()

    @staticmethod
    def hide():
        cursor.hide()

    @staticmethod
    def setCoords(x, y):
        handle = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        coords = win32console.PyCOORDType(x, y)
        handle.SetConsoleCursorPosition(coords)


    @staticmethod
    def getCoords() -> Coords:
        handle = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)
        cpos = handle.GetConsoleScreenBufferInfo()["CursorPosition"]
        return Cursor.Coords(cpos.X, cpos.Y)

    @staticmethod
    def IsConsoleValid():
        try:
            handle = win32console.GetStdHandle(win32console.STD_OUTPUT_HANDLE)  # Get current console handle id
            handle.GetConsoleScreenBufferInfo() # This will thew an error if
            return True

        except winerror as err:
            if hasattr(err, 'winerror'):
                return False

        return None

class ConsoleNotValid(Exception):
    def __str__(self):
        return f"This console is not valid to use ConsoleMenu on it 'You have to besure this python script is running in shell'"