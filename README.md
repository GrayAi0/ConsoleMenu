
# Change log
<h2>ConsoleMenu v1.0.0</h2>

- fixed: Sub-menu issues.
- fixed: Performance improved.
- update: New render method.
- update: More color options.

# menu design
<h3>Light Menu</h3>
* ligh mode running in windows Command Prompt
![Light mode by default](https://github.com/GrayAi0/ConsoleMenu/blob/main/review/Menu-light-mode.png?raw=true)
<h3>Dark Menu</h3>
* dark mode running in Windows PowerShell
![Dark mode by default](https://github.com/GrayAi0/ConsoleMenu/blob/main/review/Menu-dark-mode.png?raw=true)

# How to use
Import things you need
```py
from ConsoleMenu.menu import Menu
from ConsoleMenu.items.natives import Button
```

Create menu and append an new item
```py
itemsMenu = Menu("", (0,)) # param 2 is useless
itemMenu.appendItem(Button("Item 1"))
```

Run menu pool
```py
itemMenu.run_pool()
```

# Use settings
If you want to edit the menu settings like the characters you need to show

```py
import ConsoleMenu.settings as settings 
```

```py
new_settings = settings.default_menu_settings # This is the default settings that will be used by Menu
# Change the settings you want 
new_settings["left-character"] = "["
new_settings["right-character"] = "]"

# To applay this settings do this steps

# When you create a new menu 
# Just put the new_settings into the class init
itemMenu = Menu('Items', (0,), settings=new_settings)


# Or when you want to change it when the menu pool running
itemMenu.settings = new_settings
itemMenu._rendermenu() # Render the menu to view the new settings
```


# Example code

```py
from ConsoleMenu.menu import Menu
import ConsoleMenu.settings as pkg_settings
from ConsoleMenu.items.natives import *


characters = {}

def tms(status):
    newsettings = dict(pkg_settings.default_menu_settings)

    if status:
        newsettings["left-character"] = "I"
        newsettings["right-character"] = "I"

    menu.settings = newsettings
    menu._rendermenu()

def getValuesForStyle(key):
    if key in ["minimal_width", "minimal_height"]:
        return [i for i in range(0, 32)]
    
    if key in ['left-character', 'right-character']:
        isright = key == 'right-character'
        return [
            '|',
            ':',
            '!',
            '[' if not isright else ']'
            '(' if not isright else ')'
            '{' if not isright else '}'
            '<' if not isright else '>'
#            ...

        ]

    if key in ['top-character', 'middle-character', 'bottom-character']:
        return [
            '-',
            '_',
            '+',
            '=',
            'ـ', # This may not work
            '~',
#            ...
        ]

def exit():
    menu.running = False


menu = Menu('Menu', (0,0))



stylemenu = SubMenu("Styles", None, "Style Menu")

for key, value in zip(pkg_settings.default_menu_settings.keys(), pkg_settings.default_menu_settings.values()):
    
    def style_change(key):
        chrs = characters[key]
        chrs['index'] += 1
        if chrs['index'] > len(chrs['values'])-1:
            chrs['index'] = 0
        
        menu.settings[key] = chrs['values'][chrs['index']]
        stylemenu.settings[key] = chrs['values'][chrs['index']]
        stylemenu._rendermenu()
    

    values = getValuesForStyle(key)

    characters[key] = {
        "value": value,
        "index": 0 ,
        "values": values
    }
    vkey = key.replace('-', ' ').replace('_', ' ')
    vkey = ''.join([vkey[0].upper(), *list(vkey)[1:]])

    stylemenu.appendItem(Button(vkey, style_change, call_params=(key,)))

menu.appendItem(CheckBox('Toggel Menu style', tms, True))
menu.appendItem(stylemenu) # SubMenu have some issues
menu.appendItem(Button('Exit', exit))

menu.run_pool()
```