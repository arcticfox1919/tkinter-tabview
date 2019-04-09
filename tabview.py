import tkinter as tk
import tkinter.ttk as ttk


class TabView(tk.Frame):
    _tabs = []
    _tab_view = []
    _tab_text = []
    _current = 0  # 当前选中tab的索引
    _generate_func = None
    _select_listen = None
    _remove_listen = None

    '''
        select_listen: tab选中事件回调函数，回调函数包含一个index参数
        remove_listen: tab删除事件回调函数，返回值必须是一个布尔值，True表示删除，反之不删除
        generate_body: 生成body控件的回调函数，返回值应该是一个widget，用于添加到body中
    '''

    def __init__(self, master=None, select_listen=None,
                 remove_listen=None, generate_body=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        # 选项卡
        self._top = tk.Frame(self)
        self._top.bind("<Double-Button-1>", self._tab_add)
        self._top.pack(fill="x")

        # 分割线
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill="x")

        # 主体view
        self._bottom = tk.Frame(self)
        self._bottom.pack(fill="both", expand="yes")
        self._photo = tk.PhotoImage(file="remove.gif")

        # 事件回调
        if select_listen:
            if callable(select_listen):
                self._select_listen = select_listen
            else:
                raise Exception("select_action is not callable")

        if remove_listen:
            if callable(remove_listen):
                self._remove_listen = remove_listen
            else:
                raise Exception("remove_action is not callable")

        if generate_body:
            if callable(generate_body):
                self._generate_func = generate_body
            else:
                raise Exception("generate_body is not callable")

    # 添加选项卡
    def add_tab(self, view, text):
        self._add_body(view)
        self._create_tab(text)

    #  删除选项卡
    def remove_tab(self, index):
        self._tab_text.pop(index)

        self._tabs[index].destroy()
        self._tab_view[index].destroy()

        self._tabs.pop(index)
        self._tab_view.pop(index)

        if index > 0:
            self._current = index - 1
            self._active()

    @property
    def body(self):
        return self._bottom

    def _create_tab(self, text):
        # 选项卡单元
        tab_container = tk.Frame(self._top, relief=tk.RAISED, bd=1)

        # 标题、删除按钮
        _tab_text_view = tk.Label(tab_container, text=text, padx=8)
        _tab_remove_view = tk.Label(tab_container, image=self._photo)

        _tab_text_view.bind("<Button-1>", self._tab_click)
        _tab_remove_view.bind("<Button-1>", self._tab_remove)

        _tab_text_view.pack(side=tk.LEFT)
        _tab_remove_view.pack(side=tk.LEFT)
        tab_container.pack(side=tk.LEFT)
        self._tab_text.append(_tab_text_view)
        self._tabs.append(tab_container)
        self._active()

    def _add_body(self, view):
        self._tab_view.append(view)
        view.place(relwidth=1.0, relheight=1.0)

    # 刷新当前激活状态
    def _active(self):
        for i, item in enumerate(self._tabs):
            if i == self._current:
                item.config(relief=tk.RAISED, bd=3)
                # lift方法，让当前widget处于最顶层
                self._tab_view[self._current].lift()
            else:
                item.config(bd=1)

    def _tab_add(self, event):
        self._current = len(self._tabs)
        if not self._generate_func:
            self.add_tab(tk.Frame(self.body), "Untitled")
        else:
            self.add_tab(self._generate_func(), "Untitled")

    # 删除事件回调
    def _tab_remove(self, event):
        current_widget = event.widget.winfo_parent()
        select_index = self._index(current_widget)

        is_remove = True
        if self._remove_listen:
            is_remove = self._remove_listen(select_index)

        if is_remove:
            if select_index != -1:
                self.remove_tab(select_index)

    # 选项卡点击事件回调
    def _tab_click(self, event):
        current_widget = event.widget.winfo_parent()
        select_index = self._index(current_widget)
        if select_index != -1:
            self._current = select_index
            self._active()

            if self._select_listen:
                self._select_listen(select_index)

    # 返回当前选项卡的索引
    def _index(self, el):
        index = [i for i, x in enumerate(self._tabs) if str(x) == el]
        return index[0] if index else -1
