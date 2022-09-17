# -*- coding: utf-8 -*-
"""
Created on Wed May 19 09:52:03 2021

@author: Massimo
"""
import tkinter as tk


class MyLabelFrame(tk.LabelFrame):
    """Class rapresenting a label
       frame containing a widget"""

    def __init__(self, parent, label, widget_class,
                 widget_dict_args, widget_event_bindings=None,
                 *args, **kwargs):
        super().__init__(parent, text=label, *args, **kwargs)
        self.varibles = []
        self.selected = []
        if widget_event_bindings is None:
            widget_event_bindings = []
        self.widget = widget_class(self, **widget_dict_args)
        self.widget.grid(row=0, column=0)
        for e in widget_event_bindings:
            self.widget.bind(*e)

    def get_widget(self):
        return self.widget

    def set_(self, arg):
        if isinstance(self.widget, CheckBoxList):
            self.widget.set_(arg)
        else:
            self.widget.set('')
            self.widget['values'] = arg

    def get_values(self):
        if isinstance(self.widget, CheckBoxList):
            return self.widget.get_values()
        else:
            return self.widget.get()

    def reset(self):
        if isinstance(self.widget, CheckBoxList):
            self.widget.reset()
        else:
            # Combobox
            self.widget.set('')
            self.widget['values'] = []


class CheckBoxList(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.variables = []
        self.buttons = []
        self.selected = []

    def set_(self, name_list):
        for idx, name in enumerate(name_list):
            var = tk.IntVar()
            checkbtn = tk.Checkbutton(self, text=name, variable=var)
            self.variables.append(var)
            self.buttons.append(checkbtn)
            checkbtn.pack(side=tk.TOP, anchor='w')
            checkbtn.bind('<Button-1>', self.btn_selected)

    def reset(self):
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []

    def btn_selected(self, event):
        field = event.widget.cget('text')
        if field in self.selected:
            self.selected.remove(field)
        else:
            self.selected.append(field)

    def get_values(self):
        return self.selected
