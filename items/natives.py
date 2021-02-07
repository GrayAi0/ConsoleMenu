from .. import keyboardhandler
from ..menuitem import Item
from .. import render
from ..menu import Menu
from ..commontools import *

def _safe_call(callback=None, *args, **kw):
    return callable(callback) and None or callback(*args, **kw)

class Button(Item):

    def __init__(self, text, onclick):
        self.text = text
        self.onclick = onclick
        self.index = None
        self.menuAPI = None

    def render(self, redneroptions: dict, width) -> str:

        ldived = render.createLine(' ', int((width-len(self.text)-(len(str(self.index+1))+4))/2))
        rdived = render.createLine(' ', int((width-len(self.text)-(len(str(self.index+1))+4))/2) + (1 if len(self.text) % 2 == 0 else 0))

        button = f"{redneroptions.get('left-character', ' ')}  [{self.index+1}]{ldived}{self.text}{rdived}{redneroptions.get('right-character', ' ')}"
        return button

    def clicked(self):
        return _safe_call(self.onclick)




class CheckBox(Item):

    def __init__(self, text, on_status_changed, default_status=False):
        self.text = text
        self.onclick = on_status_changed
        self.status = default_status
        self.index = None
        self.menuAPI = None

    def render(self, redneroptions, width):

        status = f'[{self.status and "On" or "Off"}]'
        ldived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2))
        rdived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2) + (
            1 if len(self.text) % 2 == 0 else 0) - (len(status) + 2))

        button = f"{redneroptions.get('left-character', ' ')}  [{self.index + 1}]{ldived}{self.text}{rdived} {status} {redneroptions.get('right-character', ' ')}"
        return button

    def clicked(self):
        self.status = not self.status
        self.menuAPI._rendermenu()
        return _safe_call(self.onclick)


class SubMenu(Menu):

    def __init__(self, text, onenter, menu_name = None, menu_pos = None, menu_options = None):
        self.text = text
        self.onclick = onenter
        self.menuAPI = None
        super().__init__(menu_name or text, menu_pos or (0, 0), menu_options or {})
        self.AppendItem(Button("return", self._return))

    def _return(self):
        super()._remove_keys_handlers()

        print('\033[A' * (Str.getLenof('\n', self.ghostmessage) - 1), end='')
        for msg in self.menuAPI.ghostmessage:
            print(msg, end='')

        self.menuAPI.unlock()
        self.menuAPI.show()

    def render(self, redneroptions, width):

        ldived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2))
        rdived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2) + (
            1 if len(self.text) % 2 == 0 else 0) - 3)

        button = f"{redneroptions.get('left-character', ' ')}  [{self.index + 1}]{ldived}{self.text}{rdived}=> {redneroptions.get('right-character', ' ')}"
        return button

    def clicked(self):
        self.menuAPI.lock()
        self.menuAPI.hide()
        _safe_call(self.onclick)
        if not self._key_inited:
            super()._register_keys()
        self._rendermenu()

