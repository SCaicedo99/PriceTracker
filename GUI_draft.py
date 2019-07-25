from tkinter import *
import tkSimpleDialogpytho


def doNothing():
    print('Do Nothing')

# def add_item():
#     url = tk
#     return url


class WelcomePage:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.continue_old_session_button = Button(frame, text="Continue old session", command=frame.quit)
        self.continue_old_session_button.pack(side=RIGHT)
        self.start_new_session_button = Button(frame, text="Start new session", command=frame.quit)
        self.start_new_session_button.pack(side=LEFT)


class Menus:
    def __init__(self,master):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.sub_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.sub_menu)
        self.sub_menu.add_command(label="Add item", command=doNothing)
        self.sub_menu.add_command(label="Remove item", command=doNothing)
        self.sub_menu.add_separator()
        self.sub_menu.add_command(label="Exit", command=doNothing)

        self.edit_menu = Menu(self.menu)
        self.menu.add_cascade(label="Edit",menu=self.edit_menu)


class Toolbar:
    def __init__(self,master):
        self.toolbar = Frame(master, bg="blue")
        self.add_button = Button(self.toolbar, text="Add Item", command=doNothing)
        self.add_button.pack(side=LEFT, padx=2, pady=2)
        self.remove_item = Button(self.toolbar, text="Remove Item", command=doNothing)
        self.toolbar.pack(side=TOP, fill=X)


class StatusBar:
    def __init__(self,master):
        self.status = Label(master, text="Doing nothing(for now)", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)



# class NewSession:
#     def __init__(self,master):


root = Tk()
welcomeP = WelcomePage(root)

# add_item()
root.mainloop()