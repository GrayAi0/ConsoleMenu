from . import console
from .console import Cursor
import sys

class Screen:

    def __init__(self, h=32, w=32):

        if not Cursor.IsConsoleValid():
            raise console.ConsoleNotValid

        self.start_screen_pos = Cursor.getCoords()

        self.max_w = h
        self.max_h = w + self.start_screen_pos.y

        self.past_buffer = self.empty_buffer()


    def empty_buffer(self, h=-1, w=-1, letter=''):
        if h < 0:
            h = self.max_h

        if w < 0:
            w = self.max_w

        return [
            [letter] * w
            ] * h

    def _set_render_pos(self, x, y):
        Cursor.setCoords(x, y)
        

    def render_buffer(self, buffer=None, force_render=False):
        
        if not isinstance(buffer, list):
            buffer = self.empty_buffer()

        x, y = 0, self.start_screen_pos.y

        max_h, max_w = self.max_h, self.max_w

        for hindex, h in enumerate(buffer):
                
            if y >= max_h:
                break

            y += 1

            for windex, w in enumerate(h):

                if isinstance(w, Color):

                    sys.stdout.write(w.color.fg)
                    sys.stdout.write(w.color.bg)
                    continue

                x += 1
                if x >= max_w:
                    break

                self._set_render_pos(x, y)

                if force_render or w != self._get_from_past(hindex, windex):
                    sys.stdout.write(w)


            x = 0

        self.past_buffer = list(buffer)

    def _get_from_past(self, hindex, windex):
        past_buffer = self.past_buffer
        if hindex in past_buffer:
            if windex in past_buffer[hindex]:
                return past_buffer[hindex][windex]
        return ''


class Color:

    @staticmethod
    class _color:
        def __init__(self, f, g):
            self.fg = f
            self.bg = g

    def __init__(self, fg, bg, out_type):
        self.color = Color._color(fg, bg)
        self.type = out_type

    def __str__(cls):
        return cls.toString()

    def toString(self):
        return f'<{self.type}: f: {self.color.fg}, g: {self.color.bg}>'


def createLine(letter, w):
    return f'{letter}' * w
