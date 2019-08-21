import tkinter as tk
from tkinter import ttk


root = tk.Tk()

tree = ttk.Treeview(root)

tree["columns"]=("one","two")
tree.column("one", width=100)
tree.column("two", width=100)
tree.heading("one", text="column A")
tree.heading("two", text="column B")

tree.insert("" , 0,    text="Line 1", values=("1A","1b"))

id2 = tree.insert("", 1, "dir2", text="Dir 2")
tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))

##alternatively:
tree.insert("", 3, "dir3", text="Dir 3")
tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

tree.pack()
root.mainloop()

# ----------1st vid:----------
# SUMMARY: just an intro vid, getting a basic window with some text in it.
# Creating some text for the window
# theLabel = Label(root, text="This is too easy")
# theLabel.pack()  # This just packs it somewhere in the root

# ----------2nd vid:----------
# SUMMARY: it showed me the idea of frames, and how to make clickable buttons
# topFrame = Frame(root)  # This makes an invisible container
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)
#
# button1 = Button(topFrame, text="Button 1", fg="red")
# button2 = Button(topFrame, text="Button 2", fg="blue")
# button3 = Button(topFrame, text="Button 3", fg="green")
# button4 = Button(bottomFrame, text="Button 4", fg="purple")
#
# button1.pack(side=LEFT)
# button2.pack(side=LEFT)
# button3.pack(side=LEFT)
# button4.pack(side=BOTTOM)

# ----------3rd vid:----------
# SUMMARY: We created labels that where dynamic to the window size
# one = Label(root, text="One", bg="red", fg="white")  # bg = background color, fg = foreground color
# one.pack()
# two = Label(root, text="Two", bg="green", fg="black")
# two.pack(fill=X) # Is going to fill the screen as long as wide as the parent is
# three = Label(root, text="three", bg="blue", fg="white")
# three.pack(side=LEFT, fill=Y)

# ----------4th-5th vid:----------
# SUMMARY: using grid layout, input entry, checkbutton
# label_1 = Label(root, text="Name")
# label_2 = Label(root, text="Password")
# entry_1 = Entry(root)
# entry_2 = Entry(root)
#
# label_1.grid(row=0, sticky=E)
# label_2.grid(row=1, sticky=E)
#
# entry_1.grid(row=0, column=1)
# entry_2.grid(row=1, column=1)
#
# c = Checkbutton(root, text="Keep me logged in")
# c.grid(columnspan=2)

# ----------6th vid:----------
# SUMMARY: Binding functions to layouts, click button -> do something
# def printName(event):
#     print("Hello, my name is Tuo")
#
#
# button_1 = Button(root, text="Print name")
# Button-1 refers to left click of the mouse
# button_1.bind("<Button-1>", printName)
# button_1.pack()

# ----------7th vid:----------
# SUMMARY: Mouse Click Events
# def leftClick(event):
#     print("Left")
# def rightClick(event):
#     print("Right")
# def middleClick(event):
#     print("Middle")
# frame = Frame(root, width=300, height=250)
# frame.bind("<Button-1>", leftClick)
# frame.bind("<Button-2>", middleClick)
# frame.bind("<Button-3>", rightClick)
# frame.pack()

# ----------8th vid:----------
# SUMMARY: Using classes with tkinter
# class BuckysButtons:
#     def __init__(self, master):
#         frame = Frame(master)
#         frame.pack()
#         self.print_button = Button(frame, text="print Message", command=self.print_message)
#         self.print_button.pack(side=LEFT)
#         self.quit_button = Button(frame, text="Quit", command=frame.quit)
#         self.quit_button.pack(side=LEFT)
#     def print_message(self):
#         print("This works")
# b = BuckysButtons(root)

# ----------9th-11th vid:----------
# SUMMARY: Creating drop down menus, Creating a toolbar, and adding a status Bar
# def doNothing():
#     print("ok ok I won't")
#
#
# menu = Menu(root)
# root.config(menu=menu)
# sub_menu = Menu(menu)
#
# menu.add_cascade(label="File", menu=sub_menu)
# sub_menu.add_command(label="New Project...", command=doNothing)
# sub_menu.add_command(label="New...", command=doNothing)
# sub_menu.add_separator()
#
# sub_menu.add_command(label="Exit", command=doNothing)
# edit_menu = Menu(menu)
# menu.add_cascade(label="Edit", menu=edit_menu)
# edit_menu.add_command(label="redo", command=doNothing)
#
# **** ToolBar ****
#
# toolbar = Frame(root, bg="blue")
#
# insertButt = Button(toolbar, text="Insert Image", command=doNothing)
# insertButt.pack(side=LEFT, padx=2, pady=2)  # Pad gives some extra space
# printButt = Button(toolbar, text="Print Image", command=doNothing)
# printButt.pack(side=LEFT, padx=2, pady=2)  # Pad gives some extra space
#
# toolbar.pack(side=TOP, fill=X)
#
# **** Status Bar ****
#
# status = Label(root, text="Preparing to do nothing... ", bd=1, relief=SUNKEN , anchor=W)  # bd = border
# status.pack(side=BOTTOM, fill=X)

# ----------12th vid:----------
# SUMMARY: Messagebox
#
# tkinter.messagebox.showinfo("Window Title", "Monkeys can live up to 500 years")  # Okay button
#
# answer = tkinter.messagebox.askquestion("Question 1", "Do you like silly faces?")
#
# if answer == "yes":
#     print(" *---* ")

# ----------13th vid:----------
# SUMMARY: Shapes and Graphics
#
# canvas = Canvas(root, width=200, height=100)
# canvas.pack()
#
# black_line = canvas.create_line(0, 0, 200, 50)
# red_line = canvas.create_line(0, 100, 200, 50, fill="red")
# green_box = canvas.create_rectangle(25, 25, 130, 60, fill='green')
#
# canvas.delete(ALL)

# ----------14th vid:----------
# SUMMARY: Images and Icons
# photo = PhotoImage(file="add-icon-614x460.png")
# label = Label(root, image=photo)
# label.pack()