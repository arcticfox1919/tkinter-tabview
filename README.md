# tkinter-tabview

> ttk中虽然添加了`Notebook`，但其功能过于简单，无法支持双击创建选项卡，删除选项卡等功能，于是自定义了tabview，有需要的朋友，可以参考在tkinter中自定义view的方法，自定义自己的view

![](https://github.com/arcticfox1919/ImageHosting/blob/master/tabview.gif?raw=true)


使用方法
```python
import tkinter as tk
from tkinter import messagebox
from tabview import TabView


def create_body():
    global body
    return tk.Label(body, text="this is body")


def select(index):
    print("current selected -->", index)


def remove(index):
    print("remove tab -->", index)
    if messagebox.askokcancel("标题", "确定要关闭该选项卡吗？"):
        return True
    else:
        return False


root = tk.Tk()
root.geometry("640x300")

tab_view = TabView(root, generate_body=create_body,
                   select_listen=select, remove_listen=remove)

body = tab_view.body

label_1 = tk.Label(tab_view.body, text="this is tab1")
label_2 = tk.Label(tab_view.body, text="this is tab2")

# 第一个参数是向body中添加的widget, 第二个参数是tab标题
tab_view.add_tab(label_1, "tabs1")
tab_view.add_tab(label_2, "tabs2")

# TabView需要向x、y方向填充，且expand应设置为yes
tab_view.pack(fill="both", expand='yes', pady=2)

root.mainloop()
```

# tkinter-DragWindow
实现桌面可拖拽小挂件

![预览](https://github.com/arcticfox1919/ImageHosting/blob/master/DragWindow.gif?raw=true)

使用方法

```
#　导入DragWindow类
root = DragWindow()
root.set_window_size(200, 200)
root.set_display_postion(500, 400)
tk.Button(root, text="Exit", command=root.quit).pack(side=tk.BOTTOM)

root.mainloop()
```

