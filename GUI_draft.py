import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from item import AmazonItem
from multiprocessing.dummy import Pool as ThreadPool
import threading
import smtplib
import pickle


def doNothing():
    print('Do Nothing')


def calculateParallel(urls, threads=4):
    pool = ThreadPool(threads)
    results = pool.map(AmazonItem, urls)
    pool.close()
    pool.join()
    return results


def parseItem(item):
    arr = [None]*9
    arr[0] = item.title
    arr[1] = item.current_price
    arr[2] = item.highest_price
    arr[3] = item.highest_price_date
    arr[4] = item.lowest_price
    arr[5] = item.lowest_price_date
    arr[6] = item.avg_price
    arr[7] = item.availability
    arr[8] = item.url
    return arr


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
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()  # Encrypts the information.
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
    popupmsg("EMAIL HAS BEEN SENT!")
    server.quit()


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
        self.table = TableOfItems(self, controller)
        self.table.grid(row=0, column=0, rowspan=2, columnspan=2)

        table = self.table.get_table()

        buttons = ActionButtons(self, controller, tree=table.tree, table=table, items_dict=self.table.items)
        buttons.grid(row=0, column=3, rowspan=10, columnspan=3)

        controller.frames["NewSession"] = self
        controller.frames["NewSession"].grid(row=1, column=0, sticky="nsew")

    def get_name(self):
        return self.name


class OldSession(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.table = TableOfItems(self, controller=controller, file="cache.txt")
        self.table.grid(row=0, column=0, rowspan=2, columnspan=2)
        table = self.table.get_table()

        buttons = ActionButtons(self, controller, tree=table.tree, table=table, items_dict=self.table.items)
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
            parse_file = open(file, 'rb')
            prev_sess_dict = pickle.load(parse_file)
            parse_file.close()
            for item in prev_sess_dict:
                temp = AmazonItem(arr=prev_sess_dict[item])
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
    def __init__(self, parent, controller, tree, table, items_dict):
        tk.Frame.__init__(self, parent)
        self.table = table
        self.parent_name = type(parent).__name__
        self.controller = controller
        self.tree = tree
        self.items_dict = items_dict
        button1 = ttk.Button(self, text="Add Item", command=self.add_item)
        button2 = ttk.Button(self, text="Delete Item", command=self.delete_tree_item)
        button3 = ttk.Button(self, text="Send Email",
                             command=self.show_email_page)
        button4 = ttk.Button(self, text="Update Selection", command=self.update_selection)
        button5 = ttk.Button(self, text="Update All", command=self.update_all)
        button6 = ttk.Button(self, text="Back", command=lambda: controller.show_frame("WelcomePage"))
        button7 = ttk.Button(self, text="Quit", command=self.quit_window)
        self.v = tk.StringVar()

        self.e = ttk.Entry(self)
        self.v.set("Enter url here")
        self.e.config(textvariable=self.v)

        button1.grid(row=0, column=0, padx=5, pady=5)
        button2.grid(row=1, column=0, padx=5, pady=5)
        button3.grid(row=2, column=0, padx=5, pady=5)
        button4.grid(row=3, column=0, padx=5, pady=5)
        button5.grid(row=4, column=0, padx=5, pady=5)
        button6.grid(row=5, column=0, padx=5, pady=5)
        button7.grid(row=6, column=0, padx=5, pady=5)
        self.e.grid(row=0, column=1, padx=5, pady=5)

    def show_email_page(self):
        try:
            self.controller.show_frame("EmailPage")
            url = self.table.items[self.table.tree.selection()[0]].url
            self.controller.frames["EmailPage"].update_body(url)
            self.controller.frames["EmailPage"].prev_frame = self.parent_name
            self.controller.show_frame("EmailPage")
        except IndexError:
            popupmsg("Select an item!")

    def delete_tree_item(self, item=None):
        if item is not None:
            self.tree.delete(item)
        else:
            try:
                del self.tree.items[self.tree.selection()[0]]  # Delete from dictionary
                self.tree.delete(self.tree.selection()[0])  # delete from tree
            except IndexError:
                popupmsg("Select an item!")

    def add_item(self, url=None, index=None, spec_item=None):
        if spec_item is not None:
            item = spec_item
            self.items_dict[item.title] = item
            temp = self.tree.insert("", index, item.title, text=item.title,
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
            self.tree.selection_add(item.title)  # Highlights in the treeview
        elif url is not None:
            item = AmazonItem(url=url)
            self.items_dict[item.title] = item
            temp = self.tree.insert("", index, item.title, text=item.title,
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
            self.tree.selection_add(item.title)  # Highlights in the treeview

        elif self.e.get().find("amazon.com") != -1:  # Just making sure it's an amazon link
            item = AmazonItem(self.e.get().strip())
            self.items_dict[item.title] = item
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
            popupmsg("Enter valid URL")
            self.v.set("Enter url here")
            pass

    def update_all(self):
        index = 0
        urls = [None]*len(self.items_dict)
        for item in self.items_dict:  # This loop is just to get the urls
            urls[index] = self.items_dict[item].url
            index += 1

        arr_amazon_items = calculateParallel(urls)  # array with updated values items

        for am_item in arr_amazon_items:
            self.items_dict[am_item.title] = am_item  # updating values in the dictionary
            temp_index = self.tree.index(am_item.title)
            self.delete_tree_item(item=am_item.title)  # delete old item from tree
            self.add_item(index=temp_index, spec_item=am_item)  # Add updated item

    def update_selection(self):
        url = self.items_dict[self.tree.selection()[0]].url
        _index = self.tree.index(self.tree.selection()[0])
        del self.items_dict[self.tree.selection()[0]].url
        self.delete_tree_item(item=self.tree.selection()[0])
        self.add_item(url=url, index=_index)

    def quit_window(self):
        if len(self.items_dict) > 0:
            save_dict = {}
            for item in self.items_dict:
                save_dict[item.title] = parseItem(self.items_dict[item])

            print("saving to cache...")
            file_name = "cache.txt"
            file = open(file_name, 'wb')
            pickle.dump(save_dict, file)
            file.close()
            self.controller.quit()
            pass
        else:
            print("quitting...")
            self.controller.quit()


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
