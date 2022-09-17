# -*- coding: utf-8 -*-
"""
Created on Tue May 18 09:57:20 2021

@author: Massimo
"""

from application import Application

app = Application('MySQL connector')

app.attributes('-topmost', True)
app.update()
app.attributes('-topmost', False)

app.eval('tk::PlaceWindow . top')
app.mainloop()
app.close_connection()
