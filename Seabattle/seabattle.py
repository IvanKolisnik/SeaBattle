from Application import *

#ініціалізація вікна
root = Tk()
root.title = "Морський бій"
root.geometry("800x500+100+100")

#ініціалізація додатку
app = Application(master=root)
app.mainloop()
