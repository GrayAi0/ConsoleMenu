# ConsoleMenu Beta
this is just a beta version

# How to use
import things you need
```py
from ConsoleMenu.menu import Menu
from ConsoleMenu.items.natives import Button
```

create menu and append an new item
```py
itemsMenu = Menu("", (0,)) # param 2 is useless
itemMenu.AppendItem(Button("Item 1"))
```

run menu pool
```
itemMenu.loop() # this could be changed
```
