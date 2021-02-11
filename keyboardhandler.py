import threading

import keyboard as kw





keys = {

}

events_stream = open('events.log', 'w')

def _create_handler(key):
    def trigger():

        for handler in list(keys[key]["cbs"]):
            callable(handler) and handler() or None

    return trigger

def addkeylisnter(key, handler):
    if key not in keys:
        kw.add_hotkey(key, _create_handler(key))
        keys[key] = {
            "cbs": []
        }

    keys[key]["cbs"].append(handler)
    return len(keys[key]['cbs']) - 1

def removekeylisnter(key, handlerId):
    if key in keys and len(keys[key]['cbs']) > handlerId:
        del keys[key]['cbs'][handlerId]