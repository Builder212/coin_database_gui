import mysql.connector as mysql
import os

class database:
    def __init__(self):
        """
        This class will be used to work with a database in the GUI.
        To initate it, you must login with an accurate username, password, and hostname for the MySQL server.
        """
        pass

    def login(self, user, password, host):
        """
        This command will return either True or False, depending on whether the options given are correct.
        If your database doesn't exist, don't worry. As long as you have a MySQL server setup to connect too,
        this code will create a database and correct table if not already created.
        """
        try:
            self.user = user
            self.password = password
            self.host = host

            self.db = mysql.connect(
                host = self.host,
                user = self.user,
                passwd = self.password)

            cursor = self.db.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS Coin;')
            cursor.execute('USE Coin;')
            cursor.execute('CREATE TABLE IF NOT EXISTS Coins( coin_id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(20), year INT, mint VARCHAR(10), description VARCHAR(50), coin_condition VARCHAR(2), value INT, time TIMESTAMP);')
            cursor.close()
            self.db.commit()

            try:
                backup = self.backup()
            except:
                print("Beware! Your backup has failed.")

            return True
        except:
            return False

    def quit(self):
        """
        Close the database.
        """
        self.db.close()
        self.backup()

    def add(self, type, year, mint, description, coin_condition, value):
        """
        This function is used to add entries to the table in the database that has been created.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute('INSERT INTO Coins (type, year, mint, description, coin_condition, value) VALUES ("{}", {}, "{}", "{}", "{}", {});'.format(type, year, mint, description, coin_condition, value))
            cursor.close()
            self.db.commit()
            return True
        except:
            return False

    def remove(self, id):
        """
        This function will be used to remove entries in the table via their custom id.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM Coins WHERE coin_id = {};'.format(id))
            cursor.close()
            self.db.commit()
            return True
        except:
            return False

    def backup(self):
        """
        This command, when run will create a backup for your database to be used in case of corruption or loss of data.
        """
        try:
            os.system('mysqldump -u {} -p{} -h {} --databases Coin > coin_backup.sql'.format(self.user, self.password, self.host))
            return True
        except:
            return False

    def recover_from_backup(self):
        """
        This command, when run will recover your data from a backup.
        """
        try:
            os.system('mysqldump -u {} -p{} -h {} --databases Coin < coin_backup.sql'.format(self.user, self.password, self.host))
            return True
        except:
            return False

    def search(self, type, year, mint, condition, description, order_by):
        """
        This function is used to search the database's table.
        You can put in as little or as many options you like, as it is created to
        accept both blank and actual constraints. This also has an order_by value
        which is used to order the data.
        """
        if type == "":
            type='!= ""'
        else:
            type='= "{}"'.format(type)

        if year == "":
            year='!= ""'
        else:
            year='= "{}"'.format(year)

        if mint == "":
            mint='!= ""'
        else:
            mint='= "{}"'.format(mint)

        if condition == "":
            condition='!= ""'
        else:
            condition='= "{}"'.format(condition)

        if description == "":
            description='!= ""'
        else:
            description='= "{}"'.format(description)

        if order_by == "":
            order_by = ""
        else:
            order_by = 'ORDER BY {}'.format(order_by)

        cursor = self.db.cursor()
        cursor.execute('SELECT coin_id, type, year, mint, description, coin_condition, value FROM Coins WHERE type {} AND year {} AND mint {} AND description {} and coin_condition {} {};'.format(type, year, mint, description, condition, order_by))
        search = cursor.fetchall()
        cursor.close()
        self.db.commit()
        return search

    def return_db(self):
        """
        Returns the whole database.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT coin_id, type, year, mint, description, coin_condition, value FROM Coins ORDER BY coin_id;')
        all = cursor.fetchall()
        cursor.close()
        return all

    def amount_of_coins(self):
        """
        Returns the total amount of coins in the database.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT coin_id FROM Coins;')
        output = cursor.fetchall()
        cursor.close()
        amount = 0
        for val in output:
            amount += 1
        return amount

    def by_type(self):
        """
        Returns how many coins of each type are in the database.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT type FROM Coins;')
        output = cursor.fetchall()
        cursor.close()

        penny_amount = 0
        nickel_amount = 0
        dime_amount = 0
        quarter_amount = 0
        half_amount = 0
        dollar_amount = 0

        for type in output:
            if type == ('Penny',):
                penny_amount += 1
            elif type == ('Nickel',):
                nickel_amount += 1
            elif type == ('Dime',):
                dime_amount += 1
            elif type == ('Quarter',):
                quarter_amount += 1
            elif type == ('Half Dollar',):
                half_amount += 1
            elif type == ('Dollar',):
                dollar_amount += 1

        return [str(penny_amount), str(nickel_amount), str(dime_amount), str(quarter_amount), str(half_amount), str(dollar_amount)]

    def by_mint(self):
        """
        Returns the amount of coins minted in each location.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT mint FROM Coins;')
        output = cursor.fetchall()
        cursor.close()
        p = 0
        d = 0
        s = 0
        w = 0

        for type in output:
            if type == ('P',):
                p += 1
            elif type == ('D',):
                d += 1
            elif type == ('S',):
                s += 1
            elif type == ('W',):
                w += 1

        return [str(p), str(d), str(s), str(w)]

    def total_val(self):
        """
        Returns the overall value of all coins in your database.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT value FROM Coins;')
        output = cursor.fetchall()
        cursor.close()
        total = 0
        for val in output:
            if val[0] == None:
                pass
            else:
                total += val[0]
        return total

    def most_expensive(self):
        """
        Returns the value of the most expensive coin in the database.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT value FROM Coins;')
        output = cursor.fetchall()
        cursor.close()
        most_expensive = 0

        for price in output:
            worth = price[0]
            if worth > most_expensive:
                most_expensive = price[0]

        return most_expensive

    def oldest_coin(self):
        """
        Returns the year of the oldest coin in the database.
        """
        cursor = self.db.cursor()
        cursor.execute('SELECT year FROM Coins;')
        output = cursor.fetchall()
        cursor.close()
        oldest = 2000000

        for year in output:
            how_old = year[0]
            if how_old < oldest:
                oldest = year[0]

        return oldest

if __name__ == "__main__":
    db = database()
    user = input("Username: ")
    passwrd = input("Password: ")
    host = input("Host: ")
    test = db.login(user, passwrd, host)
    db.quit()
