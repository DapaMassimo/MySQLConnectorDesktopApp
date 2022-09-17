# -*- coding: utf-8 -*-
"""
Created on Tue May 18 09:33:24 2021

@author: Massimo
"""
from . import tk, ttk, m, v, pyperclip


# Controller
class Application(tk.Tk):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(title)
        self.resizable(width=False, height=False)

        self.connector = m.MySQLConnector()

        ttk.Label(self, text='MySQL gui connector',
                  font=('TkDefaultFont', 16)).grid(row=0)

        self.readform = v.ReadQueryForm(self, self.connector.get_db_list())
        self.readform.grid(row=1, padx=10, pady=10)

    def get_table_list(self, db):
        self.connector.connect_to_db(db)
        return self.connector.get_table_list()

    def get_fields(self, table):
        return self.connector.get_fields(table)

    def execute_read_query(self, query):
        result = self.connector.execute_read_query(query)
        heading = query[0] if query[0] else self.connector.get_fields(query[1])
        self.show_query_result(heading, result)

    def close_toplevel(self, toplevel_window):
        self.wm_attributes("-disabled", False)
        self.deiconify()
        toplevel_window.destroy()

    @staticmethod
    def tree_view_item_selected(event, tree):
        rowid = tree.identify_row(event.y)
        column = tree.identify_column(event.x)

        column_number = int(column[-1:]) - 1
        cur_item = tree.item(rowid)
        value = cur_item['values'][column_number]
        pyperclip.copy(value)

    def show_query_result(self, heading, result):
        self.wm_attributes("-disabled", True)
        res_w = tk.Toplevel(self)  # query result windows
        res_w.title('Query result')
        res_table = ttk.Treeview(res_w, columns=heading,
                                 show='headings', selectmode='browse')

        yscrollbar = ttk.Scrollbar(res_w, orient='vertical',
                                   command=res_table.yview)
        xscrollbar = ttk.Scrollbar(res_w, orient='horizontal',
                                   command=res_table.xview)

        res_table.configure(yscrollcommand=yscrollbar.set)
        res_table.configure(xscrollcommand=xscrollbar.set)

        for el in heading:
            res_table.heading(el, text=el)
            res_table.column(el, anchor='center', width=90, minwidth=100)

        for row in result:
            for field in row:
                res_table.insert('', 'end', values=field)

        res_table.bind('<ButtonRelease-1>',
                       lambda event: self.tree_view_item_selected(event, res_table))

        yscrollbar.pack(side=tk.RIGHT, fill='y')
        xscrollbar.pack(side=tk.BOTTOM, fill='x')
        res_table.pack()
        res_w.resizable(width=False, height=False)
        res_w.protocol('WM_DELETE_WINDOW', lambda: self.close_toplevel(res_w))

    def close_connection(self):
        self.connector.close_connection()
