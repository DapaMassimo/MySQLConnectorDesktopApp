#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:23:23 2021

@author: massimo
"""
import tkinter as tk
from tkinter import ttk
from widget import CheckBoxList
from widget import MyLabelFrame


# Views
class ReadQueryForm(tk.Frame):

    def __init__(self, parent, db_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.controller = parent

        # Use Database
        self.use_db = MyLabelFrame(self, label='Use database',
                                   widget_class=ttk.Combobox,
                                   widget_dict_args={'values': db_list,
                                                     'state': 'readonly'},
                                   widget_event_bindings=[('<<ComboboxSelected>>',
                                                           self.db_selected)])

        # Select Fields
        self.select_fields = MyLabelFrame(self, label='Select field',
                                          widget_class=CheckBoxList,
                                          widget_dict_args={})

        # From Table
        self.from_table = MyLabelFrame(self, label='From table',
                                       widget_class=ttk.Combobox,
                                       widget_dict_args={'values': [],
                                                         'state': 'readonly'},
                                       widget_event_bindings=[('<<ComboboxSelected>>',
                                                               self.table_selected)])

        # Where Fields
        self.where_fields = MyLabelFrame(self, label='Where field',
                                         widget_class=ttk.Combobox,
                                         widget_dict_args={'values': [],
                                                           'state': 'readonly'})

        # Operator
        self.operator = MyLabelFrame(self, label='Condition',
                                     widget_class=ttk.Combobox,
                                     widget_dict_args={
                                         'values': ['regexp']})

        # Condition
        self.condition = ttk.Entry(self)

        # Execute read query button
        self.execute_query = ttk.Button(self, text='Execute query',
                                        command=self.execute_query)

        self.place_components()

    def place_components(self):
        self.use_db.grid(row=1, column=0, padx=5, pady=5)
        self.from_table.grid(row=1, column=1, padx=5, pady=5)
        self.select_fields.grid(row=1, column=2, padx=5, pady=5)
        self.where_fields.grid(row=1, column=3, padx=5, pady=5)
        self.operator.grid(row=1, column=4, padx=5, pady=5)
        self.condition.grid(row=1, column=5, padx=5, pady=5)
        self.execute_query.grid(row=2, column=5, padx=5, pady=20, sticky='E')

    def execute_query(self):
        select = self.select_fields.get_values()
        from_ = self.from_table.get_values()
        where = self.where_fields.get_values()
        operator = self.operator.get_values()
        condition = self.condition.get()
        query = [select, from_, where, operator, condition]
        self.controller.execute_read_query(query)

    def db_selected(self, event):
        db = event.widget.get()
        self.from_table.set_(self.controller.get_table_list(db))
        self.select_fields.reset()
        self.where_fields.reset()

    def table_selected(self, event):
        table = event.widget.get()
        fields = self.controller.get_fields(table)

        self.select_fields.reset()
        self.select_fields.set_(fields)
        self.where_fields.set_(fields)
