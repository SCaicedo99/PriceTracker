import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from item import AmazonItem


def doNothing():
    print('Do Nothing')


class Driver(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Price Tracker")
        tk.Tk.wm_minsize(self, 600, 230)
        tk.Tk.iconbitmap(self, default='icon.ico')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold', slant='italic')
        self.col_font = tkfont.Font(family='Helvetica', size=10, weight='bold')
        container = tk.Frame(self, relief='raised', borderwidth=5)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        self.frames["WelcomePage"] = WelcomePage(parent=container, controller=self)
        self.frames["NewSession"] = NewSession(parent=container, controller=self)
        self.frames["OldSession"] = OldSession(parent=container, controller=self)

        self.frames["WelcomePage"].grid(row=1, column=0, sticky="nsew")
        self.frames["NewSession"].grid(row=1, column=0, sticky="nsew")
        self.frames["OldSession"].grid(row=1, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is Welcome Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="New Session",
                             command=lambda: controller.show_frame("NewSession"))
        button2 = ttk.Button(self, text='Old Session',
                             command=lambda: controller.show_frame("OldSession"))
        button1.pack()
        button2.pack()


class NewSession(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, height=100, width=100)
        self.controller = controller
        table = TableOfItems(self, controller)
        table.grid(row=0, column=0, rowspan=2, columnspan=2)

        buttons = ActionButtons(self, controller)
        buttons.grid(row=0, column=3, rowspan=10, columnspan=3)


class OldSession(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        table = TableOfItems(self, controller=controller, file="amazon_urls.txt")
        table.grid(row=0, column=0, rowspan=2, columnspan=2)

        buttons = ActionButtons(self, controller)
        buttons.grid(row=0, column=3, rowspan=10, columnspan=3)


class TableOfItems(tk.Frame):
    def __init__(self, parent, controller, file=None):
        tk.Frame.__init__(self, parent, background="black")
        tree = ttk.Treeview(self)
        tree["columns"]=("Price", "two")
        tree.column("Price", width=100)
        tree.column("two", width=100)
        tree.heading("Price", text="Price ($)")
        tree.pack(side="left")
        vsb = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")

        if file is not None:
            parse_file = open(file, 'r+').readlines()
            items = {}

            for url in parse_file:
                temp = AmazonItem(url)
                items[temp.title] = temp

            for key in items:
                temp = tree.insert("", "end", items[key].title, text=items[key].title,
                                   values=("${:.2f}".format(items[key].current_price)))
                tree.insert(temp, "end", text="Highest Price",
                            values=("${:.2f}".format(items[key].highest_price),
                                    items[key].highest_price_date))
                tree.insert(temp, "end", text="Lowest Price",
                            values=("${:.2f}".format(items[key].lowest_price),
                                    items[key].lowest_price_date))
                tree.insert(temp, "end", text="Average Price",
                            values=("${:.2f}".format(items[key].avg_price)))
                tree.insert(temp, "end", text="Availability",
                            values=items[key].availability)
                # indx += 1
        else:
            pass



class ActionButtons(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = ttk.Button(self, text="Add Item")
        button2 = ttk.Button(self, text="Delete Item")
        button3 = ttk.Button(self, text="Send Email")
        button4 = ttk.Button(self, text="Back", command=lambda: controller.show_frame("WelcomePage"))

        button1.grid(row=0, column=0, padx=5, pady=5)
        button2.grid(row=1, column=0, padx=5, pady=5)
        button3.grid(row=2, column=0, padx=5, pady=5)
        button4.grid(row=3, column=0, padx=5, pady=5)


class Menus:
    def __init__(self, parent):
        self.menu = tk.Menu(parent)
        parent.config(menu=self.menu)
        self.sub_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.sub_menu)
        self.sub_menu.add_command(label="Add item", command=doNothing)
        self.sub_menu.add_command(label="Remove item", command=doNothing)
        self.sub_menu.add_separator()
        self.sub_menu.add_command(label="Exit", command=doNothing)

        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)


class Toolbar:
    def __init__(self, parent):
        self.toolbar = tk.Frame(parent, bg="blue")
        self.add_button = tk.Button(self.toolbar, text="Add Item", command=doNothing)
        self.add_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.remove_item = tk.Button(self.toolbar, text="Remove Item", command=doNothing)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)


class StatusBar:
    def __init__(self,parent):
        self.status = tk.Label(parent, text="Doing nothing(for now)", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    app = Driver()
    app.mainloop()
