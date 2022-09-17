from . import controller


app = controller.Application('MySQL connector')

app.attributes('-topmost', True)
app.update()
app.attributes('-topmost', False)

app.eval('tk::PlaceWindow . top')
app.mainloop()
app.close_connection()
