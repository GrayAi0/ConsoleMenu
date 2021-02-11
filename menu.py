from . import init_vars
import sys
import time
import cursor
if init_vars.COLORED:
    import colored
else:
    colored = None

from . import keyboardhandler
from . import render
from . import settings as pkg_settings
from . import colorama
from . import console
from .commontools import *
from .console import Cursor

class Menu:

    def __init__(self, name, pos, settings={}):

        if not Cursor.IsConsoleValid():
            raise console.ConsoleNotValid

        self.name = name
        self.pos = pos
        self.settings = Dict.beshure(settings, pkg_settings.default_menu_settings)
        self.items = []
        self.selected_item = 0

        self._isLocked = False
        self._autoRender = False

        self.ghostmessage = ''
        self.screen_render = render.Screen(self.settings["maximal_height"], self.settings["maximal_width"])
        self.running = True

        self._key_inited = False
        self._registered_keys = []




    def appendItem(self, obj):
        self.items.append(obj)
        obj.index = len(self.items)-1
        obj.menuAPI = self
        if self._autoRender:
            return self._rendermenu()

    def renderlist_tobuffer(self, *_list):
        _buffer = []

        line = []

        max_w = 0
        max_h = 0
        max_ws = []

        for buffer in _list:

            for letter in buffer:
                max_h += 1

                if letter == '\n':
                    max_w += 1
                    _buffer.append(line)
                    line = []
                    max_ws.append(max_h)
                    max_h = 0
                    continue

                line.append(letter if letter != '' else ' ')

        max_h = max(*max_ws)
        screen_render = self.screen_render
        screen_render.max_w = max_h
        screen_render.max_h = max_w + screen_render.start_screen_pos.y
        screen_render.past_buffer = screen_render.empty_buffer()
        screen_render.render_buffer(_buffer, True)

    def _rendermenu(self, w=-1):

        # remove self for more speed in render
        selected_item   = self.selected_item
        settings        = self.settings
        name            = self.name


        w, h = w == -1 and settings.get("minimal_width", '0') or w, settings.get("minimal_height", '0')
        tc, lc, rc, bc = settings.get("top-character", '0'), settings.get("left-character", '1'), settings.get("right-character", '2'), settings.get("bottom-character", '3')

        normal_color, selected_color, = Colors.normal, Colors.selected

        write = [
            [normal_color],
            '\n',
        ]

        write.extend([
            lc,
            render.createLine(tc, w),
            rc, '\n'])

        ldived = render.createLine(' ', int((w - len(name)) / 2))
        rdived = render.createLine(' ', int((w - len(name)) / 2) + (2 if len(name) % 2 != 0 else 1))
        write.extend([f"{lc}{ldived}{name}{rdived}{rc}", '\n'])

        write.extend([lc, render.createLine(tc, w), rc,'\n'])


        _h = 0
        for index, item in enumerate(self.items):
            is_selected_item = selected_item == index

            renditem = item.render(settings, w)
            sep = render.createLine(' ', w)

            lines = [
                lc,
                sep,
                rc,
                '\n'
            ]

            if len(renditem) > w:
                self._rendermenu(w+(len(renditem)-w))
                return

            write.extend(lines)

            write.extend([
                lc,
                is_selected_item and [selected_color] or '',
                f"{renditem}",
                is_selected_item and [normal_color] or '',
                rc,
                [render.Color(Colors.foreground.white, Colors.background.reset, 'PIXELS_COLOR')],
                 ' <-' if is_selected_item else '   ',
                [normal_color],
                '\n',
            ])

            write.extend(lines)

            _h += Str.getLenof('\n', renditem) + 2

        if h - _h > 0:
            sep = render.createLine(' ', w)
            write.extend([[f"{lc}{sep}{rc}", '\n'] for _ in range(h - _h)])



        write.extend([render.createLine(bc, w+2), '\n'])
        self.renderlist_tobuffer(*write)

    def _up(self):
        if self._isLocked:
            return

        if self.selected_item < 1:
            self.selected_item = len(self.items)-1
        else:
            self.selected_item -= 1
        self._rendermenu()

    def _down(self):
        if self._isLocked:
            return

        if self.selected_item > len(self.items)-2:
            self.selected_item = 0
        else:
            self.selected_item += 1
        self._rendermenu()

    def _click(self):
        if self._isLocked:
            return

        self.items[self.selected_item].clicked()

    def _remove_keys_handlers(self):
        for handlerId, key in list(self._registered_keys):
            keyboardhandler.removekeylisnter(key, handlerId)
        self._key_inited = False
        self._registered_keys.clear()

    def _register_keys(self):
        self._key_inited = True
        self._registered_keys.append([keyboardhandler.addkeylisnter('up', self._up), 'up'])
        self._registered_keys.append([keyboardhandler.addkeylisnter('down', self._down), 'down'])
        self._registered_keys.append([keyboardhandler.addkeylisnter('right', self._click), 'right'])

    def run_pool(self):

        if not self._key_inited:
            self._register_keys()

        self._rendermenu()
        cursor.hide()
        self.running = True
        while self.running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

        self.hide()
        self._remove_keys_handlers()
        cursor.show()

    def setAutoRender(self, boolean):
        self._autoRender = boolean

    def unlock(self):
        self._isLocked = False

    def lock(self):
        self._isLocked = True

    def hide(self):

        screen_render = self.screen_render

        hidden_buffer = [[render.Color(colorama.Fore.RESET, colorama.Back.RESET, 'PIXELS_COLOR')]]
        hidden_buffer.extend(screen_render.empty_buffer(letter=' '))
        screen_render.render_buffer(hidden_buffer, force_render=True)
        screen_render._set_render_pos(screen_render.start_screen_pos.x, screen_render.start_screen_pos.y)

    # just call _rendermenu function
    def show(self):
        self._rendermenu()


class Colors:
    class foreground:
        reset  =  colorama.Fore.RESET

        white  =  'FG_NO_WHITE_COLOR'
        black  =  'FG_NO_BACK_COLOR'

    class background:
        reset  = colorama.Back.RESET

        white = 'BG_NO_WHITE_COLOR'
        black = 'BG_NO_BACK_COLOR'

    if colored:
        foreground.white = colored.fg('white')
        foreground.black = colored.fg('black')
        foreground.gray  = colored.fg('gray')

        background.white = colored.bg('white')
        background.black = colored.bg('black')
        background.gray  = colored.bg('gray')

    else:

        foreground.white = colorama.Fore.WHITE
        foreground.black = colorama.Fore.BLACK
        foreground.gray  = colorama.Fore.LIGHTBLACK_EX

        background.white = colorama.Back.WHITE
        background.black = colorama.Back.BLACK
        background.gray  = colorama.Back.LIGHTBLACK_EX

    if init_vars.LIGHT_MODE:
        normal = render.Color(foreground.black, background.white, 'PIXELS_COLOR')
        selected = render.Color(foreground.white, background.black, 'PIXELS_COLOR')

    else:
        normal = render.Color(foreground.white, background.black, 'PIXELS_COLOR')
        selected = render.Color(foreground.black, background.white, 'PIXELS_COLOR')

    print(selected, file=open('colors.log', 'w'))