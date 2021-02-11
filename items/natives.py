from .. import keyboardhandler
from ..menuitem import Item
from .. import render
from ..menu import Menu
from ..commontools import *

def _safe_call(callback=None,):
    
    if callback and callable(callback):
        return callback
    else:
        def _void(*args, **kw):
            return False

        return _void

class Button(Item):

    def __init__(self, text, onclick, call_params=[]):
        self.text = text
        self.onclick = onclick
        self.onparams = call_params or []
        self.index = None
        self.menuAPI = None

    def render(self, rendersettings: dict, width) -> str:

        ldived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2))
        rdived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2) + (
            0 if len(self.text) % 2 == 0 else 1))

        button = f"  [{self.index + 1}]{ldived}{self.text}{rdived}"
        return button

    def clicked(self):
        return _safe_call(self.onclick)(*self.onparams)




class CheckBox(Item):

    def __init__(self, text, on_status_changed, default_status=False):
        self.text = text
        self.onclick = on_status_changed
        self.status = default_status
        self.index = None
        self.menuAPI = None

    def render(self, rendersettings, width):

        status = f'[{self.status and "On" or "Off"}]'
        ldived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2))
        rdived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2) + (
            1 if len(self.text) % 2 == 0 else 0) - (len(status) + 1))

        button = f"  [{self.index + 1}]{ldived}{self.text}{rdived} {status} "
        return button

    def clicked(self):
        self.status = not self.status
        self.menuAPI._rendermenu()
        _safe_call(self.onclick)(self.status)


class SubMenu(Menu):

    def __init__(self, text, onenter, menu_name = None, menu_pos = None, menu_options = None):
        self.text = text
        self.onclick = onenter
        self.menuAPI = None
        super().__init__(menu_name or text, menu_pos or (0, 0), menu_options or {})
        self.appendItem(Button("return", self._return))

    def _return(self):
        super()._remove_keys_handlers()


        self.hide()
        self.menuAPI.unlock()
        self.menuAPI.show()

    def render(self, rendersettings, width):

        ldived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2))
        rdived = render.createLine(' ', int((width - len(self.text) - (len(str(self.index + 1)) + 4)) / 2) + (
            1 if len(self.text) % 2 == 0 else 0) - 4)

        button = f"  [{self.index + 1}]{ldived}{self.text}{rdived}=> "
        return button

    def clicked(self):
        self.menuAPI.lock()
        self.menuAPI.hide()
        _safe_call(self.onclick)()
        if not self._key_inited:
            super()._register_keys()
        self._rendermenu()

