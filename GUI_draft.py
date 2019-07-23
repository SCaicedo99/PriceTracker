from tkinter import *
root = Tk()


def doNothing():
    print('Do Nothing')


menu = Menu(root)
root.config(menu=menu)
sub_menu = Menu(menu)

menu.add_cascade(label="File", menu=sub_menu)
sub_menu.add_command(label="New Project...", command=doNothing)
sub_menu.add_command(label="New...", command=doNothing)
sub_menu.add_separator()

sub_menu.add_command(label="Exit", command=doNothing)
edit_menu = Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="redo", command=doNothing)

# **** ToolBar ****

toolbar = Frame(root, bg="blue")

insertButt = Button(toolbar, text="Add Item", command=doNothing)
insertButt.pack(side=LEFT, padx=2, pady=2)  # Pad gives some extra space
printButt = Button(toolbar, text="Remove Item", command=doNothing)
printButt.pack(side=LEFT, padx=2, pady=2)  # Pad gives some extra space

toolbar.pack(side=TOP, fill=X)

# **** Status Bar ****

status = Label(root, text="Preparing to do nothing... ", bd=1, relief=SUNKEN , anchor=W)  # bd = border
status.pack(side=BOTTOM, fill=X)


root.mainloop()