import sys
import time
import cursor

from . import keyboardhandler
from . import render
from . import menuitem
from . import options as pkg_options
from .commontools import *
import colorama as __in
__in.init()

class Menu:

    def __init__(self, name, pos, options={}):

        self.name = name
        self.pos = pos
        self.options = Dict.beshure(options, pkg_options.default_menu_options)

        self.items = []
        self.selected_item = 0

        self._isLocked = False
        self._autoRender = False

        self.ghostmessage = ''
        self.running = True

        self._key_inited = False
        self._registered_keys = []

    def AppendItem(self, obj):
        self.items.append(obj)
        obj.index = len(self.items)-1
        obj.menuAPI = self
        if self._autoRender:
            return self._rendermenu()

    def writeghost(self, *messages, sep=' ', end='\n'):
        message = ''
        for msg in messages:
            for chr in msg:
                message += ' ' if chr != '\n' else '\n'
                print(chr, end='')

            print(sep, end='')
        self.ghostmessage = message + end

    def clearghost(self, amount):
        print('\033[A' * (Str.getLenof('\n', amount) - 1), end='')

    def _rendermenu(self):
        self.clearghost(self.ghostmessage)
        self.ghostmessage = ''
        w, h = self.options.get("minimal_width", 0), self.options.get("minimal_height", 0)
        tc, lc, rc, bc = self.options.get("top-character", '0'), self.options.get("left-character", '1'), self.options.get("right-character", '2'), self.options.get("bottom-character", '3')

        write = render.createLine(tc, w+2) + '\n'

        ldived = render.createLine(' ', int((w - len(self.name)) / 2))
        rdived = render.createLine(' ', int((w - len(self.name)) / 2) + (1 if len(self.name) % 2 != 0 else 0))
        write += f"{lc}{ldived}{self.name}{rdived}{rc}" + '\n'

        write += render.createLine(tc, w+2) + '\n'


        _h = 0
        for index, item in enumerate(self.items):
            renditem = item.render(self.options, w)
            sep = render.createLine(' ', w)
            write += f"{lc}{sep}{rc}" + '\n'
            write += f"{renditem}  {'<-' if self.selected_item == index else '  '}" + '\n'
            _h += Str.getLenof('\n', renditem) + 2
            write += f"{lc}{sep}{rc}" + '\n'
        if h - _h > 0:
            for _ in range(h - _h):
                sep = render.createLine(' ', w)
                write += f"{lc}{sep}{rc}" + '\n'

        write += render.createLine(bc, w+2) + '\n'
        self.writeghost(write)

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

    def loop(self):

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
        print('\033[A' * (Str.getLenof('\n', self.ghostmessage) - 1), end='')
        for msg in self.ghostmessage:
            print(msg, end='')

        print('\033[A' * (Str.getLenof('\n', self.ghostmessage)), end='')

    def show(self):
        self._rendermenu()
