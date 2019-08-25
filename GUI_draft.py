import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from item import AmazonItem
import multiprocessing
import threading
import smtplib


def doNothing():
    print('Do Nothing')


def popupmsg(msg, controller):
    popup = tk.Tk()
    popup.wm_minsize(150, 85)
    popup.wm_title("!")
    popup.wm_maxsize(150, 85)
    label = ttk.Label(popup, text=msg, font=controller.NORM_FONT)
    label.pack(side="top", fill="x", pady=10, padx=12)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def send_email(controller, content, recipient):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('sebascaicedo25@gmail.com', 'vhhrbzhfcvoyffkz')

        subject = 'PriceTracker reminder!'
        body = content

        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(
            'sebascaicedo25@gmail.com',
            recipient,
            msg
        )
        print("EMAIL HAS BEEN SENT!")

        server.quit()
    except IndexError:
        popupmsg("Select something", controller)


class Driver(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Price Tracker")
        tk.Tk.wm_minsize(self, 600, 230)
        tk.Tk.iconbitmap(self, default='icon.ico')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight='bold', slant='italic')
        self.NORM_FONT = tkfont.Font(family="Helvetica", size=10)
        self.container = tk.Frame(self, relief='raised', borderwidth=5)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["WelcomePage"] = WelcomePage(parent=self.container, controller=self)
        self.frames["LoadingScreen"] = LoadingScreen(parent=self.container, controller=self)
        self.frames["EmailPage"] = EmailPage(parent=self.container, controller=self)

        self.frames["WelcomePage"].grid(row=1, column=0, sticky="nsew")
        self.frames["LoadingScreen"].grid(row=1, column=0, sticky="nsew")
        self.frames["EmailPage"].grid(row=1, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def init_new_session(self):
        if 'NewSession' not in self.frames:
            NewSession(parent=self.container, controller=self)
            # self.frames["NewSession"] = NewSession(parent=self.container, controller=self)
            # self.frames["NewSession"].grid(row=1, column=0, sticky="nsew")
        else:
            self.show_frame("NewSession")

    def init_old_session(self):
        if "OldSession" not in self.frames:
            # TODO If there is time, make the loading screen work
            # temp_process = multiprocessing.Process(target=OldSession, args=(self.container,
            #                                                  self))
            # temp_process.start()
            # self.show_frame()
            OldSession(parent=self.container, controller=self)
        else:
            self.show_frame("OldSession")


class LoadingScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Loading...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        self.progress_bar.pack(expand="True", fill="x", side=tk.TOP)

    def start_bar(self):
        self.progress_bar.start(50)

    def stop_bar(self):
        self.progress_bar.stop()


class EmailPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.prev_frame = "WelcomePage"
        self.controller = controller
        label1 = tk.Label(self, text="Edit Email ", font=controller.title_font)
        label2 = tk.Label(self, text="Email content ")
        label3 = tk.Label(self, text="Recipient ")
        email_text = tk.Text(self, width=40, height=1)
        email_text.insert(tk.END, "example@example.com")
        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(self.prev_frame))
        button2 = ttk.Button(self, text="Send Email", command=lambda:
                             send_email(controller, self.text.get("1.0",
                                        tk.END).strip(), email_text.get("1.0", tk.END).strip()))
        body = "Check out this link: "
        self.text = tk.Text(self, width=40, height=10, wrap="word")
        self.text.insert(tk.END, body)

        label1.grid(row=0, column=0, padx=20)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)
        email_text.grid(row=2, column=1)
        self.text.grid(row=1, column=1)
        button1.grid(row=3, column=2, pady=4)
        button2.grid(row=3, column=1, pady=5)



        controller.frames["EmailPage"] = self
        controller.frames["EmailPage"].grid(row=1, column=0, sticky="nsew")

    def update_body(self, url):
        self.text.insert(tk.END, url)


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is Welcome Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="New Session",
                             command=controller.init_new_session)
        button2 = ttk.Button(self, text='Old Session',
                             command=controller.init_old_session)
        button3 = ttk.Button(self, text="Show loading screen",
                             command=lambda: controller.show_frame("LoadingScreen"))
        button1.pack()
        button2.pack()
        button3.pack()


class NewSession(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, height=100, width=100)
        self.name = "NewSession"
        self.controller = controller
        table = TableOfItems(self, controller)
        table.grid(row=0, column=0, rowspan=2, columnspan=2)
        tree = table.get_tree()

        buttons = ActionButtons(self, controller, tree=self.table.tree, table=table)
        buttons.grid(row=0, column=3, rowspan=10, columnspan=3)

        controller.frames["NewSession"] = self
        controller.frames["NewSession"].grid(row=1, column=0, sticky="nsew")

    def get_name(self):
        return self.name


class OldSession(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        table = TableOfItems(self, controller=controller, file="amazon_urls.txt")
        table.grid(row=0, column=0, rowspan=2, columnspan=2)
        table = table.get_table()

        buttons = ActionButtons(self, controller, tree=table.tree, table=table)
        buttons.grid(row=0, column=3, rowspan=10, columnspan=3)

        controller.frames["OldSession"] = self
        controller.frames["OldSession"].grid(row=1, column=0, sticky="nsew")

    def get_name(self):
        return self.name


class TableOfItems(tk.Frame):
    def __init__(self, parent, controller, file=None):
        tk.Frame.__init__(self, parent, background="black")
        self.tree = ttk.Treeview(self)
        self.tree["columns"]=("Price", "two")
        self.tree.column("Price", width=100)
        self.tree.column("two", width=100)
        self.tree.heading("Price", text="Price ($)")
        self.tree.pack(side="left")
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.items = {}
        if file is not None:
            parse_file = open(file, 'r+').readlines()

            for url in parse_file:
                temp = AmazonItem(url)
                self.items[temp.title] = temp

            for key in self.items:
                temp_thread = threading.Thread(target=self.populate_tree,
                                               args=(self.items[key],))
                temp_thread.start()
        else:
            pass

    def populate_tree(self, item):
        temp = self.tree.insert("", "end", item.title, text=item.title,
                                values=("${:.2f}".format(item.current_price)))
        self.tree.insert(temp, "end", text="Highest Price",
                         values=("${:.2f}".format(item.highest_price),
                                 item.highest_price_date))
        self.tree.insert(temp, "end", text="Lowest Price",
                         values=("${:.2f}".format(item.lowest_price),
                                 item.lowest_price_date))
        self.tree.insert(temp, "end", text="Average Price",
                         values=("${:.2f}".format(item.avg_price)))
        self.tree.insert(temp, "end", text="Availability",
                         values=item.availability)

    def get_table(self):
        return self


class ActionButtons(tk.Frame):
    def __init__(self, parent, controller, tree, table):
        tk.Frame.__init__(self, parent)
        self.table = table
        self.parent_name = type(parent).__name__
        self.controller = controller
        self.tree = tree
        button1 = ttk.Button(self, text="Add Item", command=self.add_item)
        button2 = ttk.Button(self, text="Delete Item", command=self.delete_tree_item)
        button3 = ttk.Button(self, text="Send Email",
                             command=self.show_email_page)
        button4 = ttk.Button(self, text="Back", command=lambda: controller.show_frame("WelcomePage"))
        self.v = tk.StringVar()

        self.e = ttk.Entry(self)
        self.v.set("Enter url here")
        self.e.config(textvariable=self.v)

        button1.grid(row=0, column=0, padx=5, pady=5)
        button2.grid(row=1, column=0, padx=5, pady=5)
        button3.grid(row=2, column=0, padx=5, pady=5)
        button4.grid(row=3, column=0, padx=5, pady=5)
        self.e.grid(row=0, column=1, padx=5, pady=5)

    def show_email_page(self):
        self.controller.show_frame("EmailPage")
        url = self.table.items[self.table.tree.selection()[0]].url
        self.controller.frames["EmailPage"].update_body(url)
        self.controller.frames["EmailPage"].prev_frame = self.parent_name
        self.controller.show_frame("EmailPage")

    def delete_tree_item(self):
        try:
            self.tree.delete(self.tree.selection()[0])
        except IndexError:
            pass

    def add_item(self):
        if self.e.get().find("amazon.com") != -1:  # Just making sure it's an amazon link
            item = AmazonItem(self.e.get().strip())
            self.e.delete(0, tk.END)
            temp = self.tree.insert("", "end", item.title, text=item.title,
                                    values=("${:.2f}".format(item.current_price)))
            self.tree.insert(temp, "end", text="Highest Price",
                             values=("${:.2f}".format(item.highest_price),
                                     item.highest_price_date))
            self.tree.insert(temp, "end", text="Lowest Price",
                             values=("${:.2f}".format(item.lowest_price),
                                     item.lowest_price_date))
            self.tree.insert(temp, "end", text="Average Price",
                             values=("${:.2f}".format(item.avg_price)))
            self.tree.insert(temp, "end", text="Availability",
                             values=item.availability)
            self.v.set("Enter url here")
        else:
            self.v.set("Enter url here")
            pass


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
    def __init__(self, parent):
        self.status = tk.Label(parent, text="Doing nothing(for now)", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    app = Driver()
    app.mainloop()
