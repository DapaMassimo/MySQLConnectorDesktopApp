from . import controller

def start():
    app = controller.Application('MySQL connector')

    app.attributes('-topmost', True)
    app.update()
    app.attributes('-topmost', False)

    app.eval('tk::PlaceWindow . top')
    app.mainloop()
    app.close_connection()
