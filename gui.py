import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, Spinbox
from tkinter import messagebox as msg
from time import sleep
from database import database as db

class gui:
    def __init__(self):
        """
        Initiates the gui.
        """
        self.win = tk.Tk()
        self.win.title("Coin Database")

        self.db = db()

        self.create_widgets()

    def _quit(self):
        """
        This safely quits the program.
        """
        self.win.quit()
        self.win.destroy()
        try:
            self.db.quit()
        except:
            pass
        exit()

    def login(self):
        """
        This function is called on the login page to login to the database.
        """
        login_attempt = self.db.login(self.username.get(), self.password.get(), self.ip.get())
        if login_attempt == True:
            self.tab_control.tab(1, state="normal")
            self.tab_control.tab(2, state="normal")
            self.tab_control.tab(3, state="normal")
            self.tab_control.tab(4, state="normal")
            self.tab_control.tab(0, state="disabled")
            self.password_entry.delete(0, 'end')

            result = self.db.return_db()
            output = "Your results:\n"
            for id, type, year, mint, description, condition, value in result:
                output += '{} - {} - {} - {} - {} - {} - {}\n'.format(id, type, year, mint, description, condition, value)
            output += "\n"

            self.all.configure(state ='normal')
            self.all.insert(tk.INSERT, output)
            self.all.configure(state ='disabled')

            self.over_tab()

        else:
            msg.showwarning('Incorrect Login', 'Your username, password, and or host ID is incorrect. Please Try again with the correct login.')

    def logout(self):
        """
        This function is called by the menu to logout.
        """
        try:
            self.tab_control.tab(0, state="normal")
            self.tab_control.tab(1, state="disabled")
            self.tab_control.tab(2, state="disabled")
            self.tab_control.tab(3, state="disabled")
            self.tab_control.tab(4, state="disabled")
            self.password_entry.delete(0, 'end')
            self.db.quit()
        except:
            msg.showwarning('Logout Error', 'You are not logged in. You have no need to logout.')

    def backup_db(self):
        """
        This function is called by the Backup Database button on the overview to backup the database.
        """
        try:
            self.db.backup()
        except:
            msg.showwarning('Backup Error', 'Your backup attempt has failed.')

    def recover_db(self):
        """
        This function is called to recover the database form a backup
        """
        try:
            self.db.recover_from_backup()
        except:
            msg.showwarning('Recovery Error', 'Your recovery attempt has failed.')

    def insert_coin(self):
        """
        This function is used to insert a coin into the database.
        """
        if self.type.get() == "" or self.condition.get() == "" or self.description.get() == "":
            msg.showwarning('Blank Values', 'You have failed to either give this entry a type, condition, or description.')

        else:
            self.db.add(self.type.get(), self.year.get(), self.mint.get(), self.description.get(), self.condition.get(), self.value.get())
            self.scr.configure(state ='normal')
            self.scr.insert(tk.INSERT, "Coin added.\n")
            self.scr.configure(state ='disabled')
            self.type_chosen.set('')
            self.mint_chosen.set('')
            self.condition_chosen.set('')
            self.year_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')
            self.value_entry.delete(0, 'end')

    def remove_coin(self):
        """
        This function is used to remove a coin from the database.
        """
        try:
            self.db.remove(self.id.get())
            self.scr.configure(state ='normal')
            self.scr.insert(tk.INSERT, "Coin {} removed.\n".format(self.id.get()))
            self.scr.configure(state ='disabled')
            self.id_entry.delete(0, 'end')
        except:
            msg.showwarning('Blank Value', 'You have failed to enter a valid id.')

    def search_db(self):
        """
        This function is called to search the database and return the results.
        """
        self.sort_scr.configure(state ='normal')
        self.sort_scr.delete('0.0', tk.END)
        self.sort_scr.configure(state ='disabled')
        if self.sort_by.get() == 0:
            sort = "coin_id"
        elif self.sort_by.get() == 1:
            sort = "type"
        elif self.sort_by.get() == 2:
            sort = "year"
        elif self.sort_by.get() == 3:
            sort = "mint"
        elif self.sort_by.get() == 4:
            sort = "coin_condition"
        elif self.sort_by.get() == 5:
            sort = "value"
        else:
            sort = ""

        result = self.db.search(self.search_type.get(), self.search_year.get(), self.search_mint.get(), self.search_condition.get(), self.description_search.get(), sort)
        output = "Your results:\n"

        for id, type, year, mint, description, condition, value in result:
            output += '{} - {} - {} - {} - {} - {} - {}\n'.format(id, type, year, mint, description, condition, value)
        output += "\n"

        self.sort_scr.configure(state ='normal')
        self.sort_scr.insert(tk.INSERT, output)
        self.sort_scr.configure(state ='disabled')

    def show_db(self):
        """
        This function is called to return the whole database.
        """
        self.all.configure(state ='normal')
        self.all.delete('0.0', tk.END)
        self.all.configure(state ='disabled')

        result = self.db.return_db()
        output = "Your results:\n"

        for id, type, year, mint, description, condition, value in result:
            output += '{} - {} - {} - {} - {} - {} - {}\n'.format(id, type, year, mint, description, condition, value)
        output += "\n"

        self.all.configure(state ='normal')
        self.all.insert(tk.INSERT, output)
        self.all.configure(state ='disabled')

    def update_overview(self):
        """
        This function is called to update the overview tab.
        """
        self.all_label.destroy()
        self.old_label.destroy()
        self.value_label.destroy()
        self.type_label.destroy()
        self.mint_label.destroy()

        all = "You have {} coins in your database.".format(self.db.amount_of_coins())
        self.all_label = ttk.Label(self.overview_tab, text=all)
        self.all_label.grid(column=0, row=0, padx=2, pady=2)

        oldest = "Your oldest coin is from {}.".format(self.db.oldest_coin())
        self.old_label = ttk.Label(self.overview_tab, text=oldest)
        self.old_label.grid(column=0, row=1, padx=2, pady=2)

        worth = "Your collection of coins is worth ${}. Your most expensive coin is worth ${}.".format(self.db.total_val(), self.db.most_expensive())
        self.value_label = ttk.Label(self.overview_tab, text=worth)
        self.value_label.grid(column=0, row=2, padx=2, pady=2, columnspan=2)

        type_amount = self.db.by_type()
        types = ['Penny - ', 'Nickel - ', 'Dime - ', 'Quarter - ', 'Half Dollar - ', 'Dollar - ']
        by_type = ""
        for x in range(6):
            by_type += types[x]+"{}\n".format(type_amount[x])
        self.type_label = ttk.Label(self.type_group, text=by_type)
        self.type_label.grid(column=0, row=0, padx=2, pady=2)

        mint_amount = self.db.by_mint()
        mints = ['Philadelphia - ', 'Denver - ', 'San Francisco - ', 'West Point - ']
        by_mint = ""
        for x in range(4):
            by_mint += mints[x]+"{}\n".format(mint_amount[x])
        self.mint_label = ttk.Label(self.mint_group, text=by_mint)
        self.mint_label.grid(column=0, row=0, padx=2, pady=2)


    def create_widgets(self):
        """
        Creates the tabs needed.
        """
        self.tab_control = ttk.Notebook(self.win)

        self.login_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.login_tab, text='Login')
        self.overview_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text='Overview')
        self.entry_tab = ttk.Frame(self.tab_control)
        self.view_all = ttk.Frame(self.tab_control)
        self.tab_control.add(self.view_all, text='View All Coins')
        self.tab_control.add(self.entry_tab, text='Add/Remove Coin')
        self.search_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.search_tab, text='Search Coins')

        self.tab_control.pack(expand=1, fill="both")

        self.tab_control.tab(0, state="normal")
        self.tab_control.tab(1, state="disabled")
        self.tab_control.tab(2, state="disabled")
        self.tab_control.tab(3, state="disabled")
        self.tab_control.tab(4, state="disabled")

        self.login_db_tab()
        self.view_tab()
        self.add_remove_tab()
        self.search_db_tab()
        self.menu()


    def login_db_tab(self):
        """
        Creates the widgets that will be on the login tab.
        """
        #login group
        login = ttk.LabelFrame(self.login_tab, text=' Login ')
        login.grid(column=0, row=0, padx=8, pady=4)

        #Labels
        ttk.Label(login, text="Username:").grid(column=0, row=0, padx=2, pady=2)
        ttk.Label(login, text="Password:").grid(column=0, row=1, padx=2, pady=2)
        ttk.Label(login, text="Host IP:").grid(column=0, row=2, padx=2, pady=2)

        #entry
        self.username = tk.StringVar()
        self.username_entry = ttk.Entry(login, width=20, textvariable=self.username)
        self.username_entry.grid(column=1, row=0, padx=2, pady=2)

        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(login, show="*", width=20, textvariable=self.password)
        self.password_entry.grid(column=1, row=1, padx=2, pady=2)

        self.ip = tk.StringVar()
        self.ip_entry = ttk.Entry(login, width=20, textvariable=self.ip)
        self.ip_entry.grid(column=1, row=2, padx=2, pady=2)

        #login button
        self.login_to_db = ttk.Button(login, text="Login", command=self.login)
        self.login_to_db.grid(column=0, row=3, padx=2, pady=2, columnspan=2)

    def over_tab(self):
        """
        Creates the widgets that will be on the Overview tab.
        """
        all = "You have {} coins in your database.".format(self.db.amount_of_coins())
        self.all_label = ttk.Label(self.overview_tab, text=all)
        self.all_label.grid(column=0, row=0, padx=2, pady=2)

        oldest = "Your oldest coin is from {}.".format(self.db.oldest_coin())
        self.old_label = ttk.Label(self.overview_tab, text=oldest)
        self.old_label.grid(column=0, row=1, padx=2, pady=2)

        worth = "Your collection of coins is worth ${}. Your most expensive coin is worth ${}.".format(self.db.total_val(), self.db.most_expensive())
        self.value_label = ttk.Label(self.overview_tab, text=worth)
        self.value_label.grid(column=0, row=2, padx=2, pady=2, columnspan=2)

        self.type_group = ttk.LabelFrame(self.overview_tab, text=' Coins by type: ')
        self.type_group.grid(column=0, row=3)
        self.mint_group = ttk.LabelFrame(self.overview_tab, text=' Coins by mint: ')
        self.mint_group.grid(column=1, row=3)

        type_amount = self.db.by_type()
        types = ['Penny - ', 'Nickel - ', 'Dime - ', 'Quarter - ', 'Half Dollar - ', 'Dollar - ']
        by_type = ""
        for x in range(6):
            by_type += types[x]+"{}\n".format(type_amount[x])
        self.type_label = ttk.Label(self.type_group, text=by_type)
        self.type_label.grid(column=0, row=0, padx=2, pady=2)

        mint_amount = self.db.by_mint()
        mints = ['Philadelphia - ', 'Denver - ', 'San Francisco - ', 'West Point - ']
        by_mint = ""
        for x in range(4):
            by_mint += mints[x]+"{}\n".format(mint_amount[x])
        self.mint_label = ttk.Label(self.mint_group, text=by_mint)
        self.mint_label.grid(column=0, row=0, padx=2, pady=2)

        self.update = ttk.Button(self.overview_tab, text="Update Information", command=self.update_overview)
        self.update.grid(column=0, row=4, padx=2, pady=2)

        self.backup = ttk.Button(self.overview_tab, text="Backup Database", command=self.backup_db)
        self.backup.grid(column=0, row=5, padx=2, pady=2)

        self.recover = ttk.Button(self.overview_tab, text="Recover Database", command=self.recover_db)
        self.recover.grid(column=0, row=6, padx=2, pady=2)

    def view_tab(self):
        """
        Creates the widgets that will be on the View All Coins tab.
        """
        self.add_coin = ttk.Button(self.view_all, text="Update View", command=self.show_db)
        self.add_coin.grid(column=0, row=0, padx=2, pady=2)

        self.all = scrolledtext.ScrolledText(self.view_all, width=70, height=19, wrap=tk.WORD, state="disabled")
        self.all.grid(column=0, row=1)

    def add_remove_tab(self):
        """
        Creates the widgets that will be on the Add/Remove Coin tab.
        """
        #entry group
        entry = ttk.LabelFrame(self.entry_tab, text=' Add Coin ')
        entry.grid(column=0, row=0, padx=8, pady=4)

        #Labels
        ttk.Label(entry, text="Type:").grid(column=0, row=0)
        ttk.Label(entry, text="Year:").grid(column=1, row=0)
        ttk.Label(entry, text="Mint:").grid(column=2, row=0)
        ttk.Label(entry, text="Condition:").grid(column=3, row=0)
        ttk.Label(entry, text="Value:").grid(column=4, row=0)
        ttk.Label(entry, text="Description:").grid(column=0, row=2)

        #type dropdown menu
        self.type = tk.StringVar()
        self.type_chosen = ttk.Combobox(entry, width=10, textvariable=self.type, state='readonly')
        self.type_chosen['values'] = ('Penny', 'Nickel', 'Dime', 'Quarter', 'Half Dollar', 'Dollar')
        self.type_chosen.grid(column=0, row=1, padx=2, pady=2)

        #year entry
        self.year = tk.StringVar()
        self.year_entry = ttk.Entry(entry, width=4, textvariable=self.year)
        self.year_entry.grid(column=1, row=1, padx=2, pady=2)

        #mint dropdown menu
        self.mint = tk.StringVar()
        self.mint_chosen = ttk.Combobox(entry, width=4, textvariable=self.mint, state='readonly')
        self.mint_chosen['values'] = ('P', 'D', 'S', 'W')
        self.mint_chosen.grid(column=2, row=1, padx=2, pady=2)

        #condition dropdown menu
        self.condition = tk.StringVar()
        self.condition_chosen = ttk.Combobox(entry, width=4, textvariable=self.condition, state='readonly')
        self.condition_chosen['values'] = ('PR', 'FA', 'AG', 'G', 'VG', 'F', 'VF', 'XF', 'AU', 'U', 'MS', 'PR')
        self.condition_chosen.grid(column=3, row=1, padx=2, pady=2)

        #value entry
        self.value = tk.StringVar()
        self.value_entry = ttk.Entry(entry, width=6, textvariable=self.value)
        self.value_entry.grid(column=4, row=1, padx=2, pady=2)

        #description entry
        self.description = tk.StringVar()
        self.description_entry = ttk.Entry(entry, width=50, textvariable=self.description)
        self.description_entry.grid(column=0, row=3, columnspan=5, padx=2, pady=2)

        #add coin to database
        self.add_coin = ttk.Button(entry, text="Add Coin", command=self.insert_coin)
        self.add_coin.grid(column=0, row=4, padx=2, pady=2)

        #remove group
        remove = ttk.LabelFrame(self.entry_tab, text=' Remove Coin ')
        remove.grid(column=0, row=1, pady=4, columnspan=4)

        #Labels
        ttk.Label(remove, text="Coin ID:").grid(column=0, row=0, padx=2, pady=2)

        #enter id
        self.id = tk.StringVar()
        self.id_entry = ttk.Entry(remove, width=4, textvariable=self.id)
        self.id_entry.grid(column=2, row=0, padx=2, pady=2)

        #remove coin from database
        self.remove_coin = ttk.Button(remove, text="Remove Coin", command=self.remove_coin)
        self.remove_coin.grid(column=3, row=0, padx=2, pady=2)

        #output from removing
        self.scr = scrolledtext.ScrolledText(self.entry_tab, width=48, height=9, wrap=tk.WORD, state="disabled")
        self.scr.grid(column=0, row=2, columnspan=4)

    def search_db_tab(self):
        """
        Creates the widgets that will be on the Search Coins tab.
        """
        #search group
        search = ttk.LabelFrame(self.search_tab, text=' Search Coin Database ')
        search.grid(column=0, row=0, padx=8, pady=4)

        #Labels
        ttk.Label(search, text="Type:").grid(column=0, row=0, padx=2, pady=2)
        ttk.Label(search, text="Year:").grid(column=1, row=0, padx=2, pady=2)
        ttk.Label(search, text="Mint:").grid(column=2, row=0, padx=2, pady=2)
        ttk.Label(search, text="Condition:").grid(column=3, row=0, padx=2, pady=2)
        ttk.Label(search, text="Description:").grid(column=0, row=2, padx=2, pady=2)

        #type dropdown menu
        self.search_type = tk.StringVar()
        self.type_search = ttk.Combobox(search, width=10, textvariable=self.search_type, state='readonly')
        self.type_search['values'] = ('', 'Penny', 'Nickel', 'Dime', 'Quarter', 'Half Dollar', 'Dollar')
        self.type_search.grid(column=0, row=1, padx=2, pady=2)

        #year entry
        self.search_year = tk.StringVar()
        self.year_search = ttk.Entry(search, width=4, textvariable=self.search_year)
        self.year_search.grid(column=1, row=1, padx=2, pady=2)

        #mint dropdown menu
        self.search_mint = tk.StringVar()
        self.mint_search = ttk.Combobox(search, width=4, textvariable=self.search_mint, state='readonly')
        self.mint_search['values'] = ('', 'P', 'D', 'S', 'W')
        self.mint_search.grid(column=2, row=1, padx=2, pady=2)

        #condition dropdown menu
        self.search_condition = tk.StringVar()
        self.condition_search = ttk.Combobox(search, width=4, textvariable=self.search_condition, state='readonly')
        self.condition_search['values'] = ('', 'PR', 'FA', 'AG', 'G', 'VG', 'F', 'VF', 'XF', 'AU', 'U', 'MS', 'PR')
        self.condition_search.grid(column=3, row=1, padx=2, pady=2)

        #search button
        self.remove_coin = ttk.Button(self.search_tab, text="Search!", command=self.search_db)
        self.remove_coin.grid(column=1, row=0, padx=2, pady=2)

        #sort by
        sort = ttk.LabelFrame(self.search_tab, text=' Sort By ')
        sort.grid(column=0, row=1, padx=8, pady=4, columnspan=2)

        #check buttons
        self.sort_by = tk.IntVar()
        self.type_sort = tk.Radiobutton(sort, text='Value', variable=self.sort_by, value=5)
        self.type_sort.grid(column=5, row=0)
        self.type_sort = tk.Radiobutton(sort, text='Type', variable=self.sort_by, value=1)
        self.type_sort.grid(column=1, row=0)
        self.year_sort = tk.Radiobutton(sort, text='Year', variable=self.sort_by, value=2)
        self.year_sort.grid(column=2, row=0)
        self.mint_sort = tk.Radiobutton(sort, text='Mint', variable=self.sort_by, value=3)
        self.mint_sort.grid(column=3, row=0)
        self.condition_sort = tk.Radiobutton(sort, text='Condition', variable=self.sort_by, value=4)
        self.condition_sort.grid(column=4, row=0)
        self.id_sort = tk.Radiobutton(sort, text='ID', variable=self.sort_by, value=0)
        self.id_sort.grid(column=0, row=0)

        self.description_search = tk.StringVar()
        self.description_sort = ttk.Entry(search, width=50, textvariable=self.description_search)
        self.description_sort.grid(column=0, row=3, columnspan=4, padx=2, pady=2)

        #search output
        self.sort_scr = scrolledtext.ScrolledText(self.search_tab, width=70, height=11, wrap=tk.WORD, state="disabled")
        self.sort_scr.grid(column=0, row=3, columnspan=4)

    def menu(self):
        """
        Creates the menu.
        """
        #menu
        menu_bar = Menu(self.win)
        self.win.config(menu=menu_bar)

        #file menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self._quit)
        menu_bar.add_cascade(label="File", menu=file_menu)


if __name__ == "__main__":
    gui = gui()
    gui.win.mainloop()
