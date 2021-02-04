from log import log_to_file as log
from errors import *
import mysql.connector as mysql
import os, datetime

class database:
    def __init__(self, db_name):
        """
        This class will be used to work with a database in the GUI.
        To initate it, you must login with an accurate username, password, and hostname for the MySQL server.
        """
        self.name = db_name
        log.log('logs.txt', 'Class database initiated on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))

    def login(self, user, password, host):
        """
        This function will return nothing, but to use this make sure to use the try and except brackets when running this.
        If LoginError has been raised, then there was an error while logging in. If DatabaseError was raised, there was an
        issue in making sure the database was created. If BackupError is raised, then there was an issue in backing up the
        database. The goal of this is to establish a connection with the database, make sure the correct tables are setup,
        and backup the database.
        """
        self.user = user
        self.password = password
        self.host = host

        try:
            self.db = mysql.connect(
                host = self.host,
                user = self.user,
                passwd = self.password)
        except:
            raise LoginError
            log.log('error.txt', 'Failure to log into database on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))
        else:
            log.log('logs.txt', 'Login to database successful on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))
            try:
                cursor = self.db.cursor()
                cursor.execute('CREATE DATABASE IF NOT EXISTS {};'.format(self.name))
                cursor.execute('USE {};'.format(self.name))
                cursor.execute('CREATE TABLE IF NOT EXISTS Coins( coin_id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(20), year INT, mint VARCHAR(10), description VARCHAR(50), coin_condition VARCHAR(2), value INT, time TIMESTAMP);')
                cursor.close()
                self.db.commit()
            except:
                raise DatabaseError
                log.log('error.txt', 'Failure to setup database on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))
            else:
                log.log('logs.txt', 'Database setup successfully on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))

            try:
                backup = self.backup()
            except BackupFailed:
                raise BackupError
            else:
                log.log('logs.txt', 'Backup successful on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))

    def backup(self):
        """
        This command, when run will create a backup for your database to be used in case of corruption or loss of data.
        If the backup errors out it will raise BackupFailed.
        """
        try:
            os.system('mysqldump -u {0} -p{1} -h {2} --databases {3} > {3}_backup.sql'.format(self.user, self.password, self.host, self.name))
        except:
            raise BackupFailed
            log.log('error.txt', 'Failure to complete backup on {} at {}.\n'.format(str(datetime.datetime.now()).split(" ")[0], str(datetime.datetime.now()).split(" ")[1]))

    def quit(self):
        """
        Close the database.
        """
        try:
            self.db.close()
        except:
            raise QuitError
        else:
            try:
                self.backup()
            except BackupFailed:
                raise BackupError


    def add(self, type, year, mint, description, coin_condition, value):
        """
        This function is used to add entries to the table in the database that has been created.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute('INSERT INTO Coins (type, year, mint, description, coin_condition, value) VALUES ("{}", {}, "{}", "{}", "{}", {});'.format(type, year, mint, description, coin_condition, value))
            cursor.close()
            self.db.commit()
        except:
            raise AddError

    def remove(self, id):
        """
        This function will be used to remove entries in the table via their custom id.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM Coins WHERE coin_id = {};'.format(id))
            cursor.close()
            self.db.commit()
        except:
            raise RemoveError

    def recover_from_backup(self):
        """
        This command, when run will recover your data from a backup.
        """
        try:
            os.system('mysqldump -u {} -p{} -h {} --databases Coin < coin_backup.sql'.format(self.user, self.password, self.host))
        except:
            raise RecoverError

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

        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT coin_id, type, year, mint, description, coin_condition, value FROM Coins WHERE type {} AND year {} AND mint {} AND description {} and coin_condition {} {};'.format(type, year, mint, description, condition, order_by))
            search = cursor.fetchall()
            cursor.close()
            self.db.commit()
            return search
        except:
            raise SearchError

    def return_db(self):
        """
        Returns the whole database.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT coin_id, type, year, mint, description, coin_condition, value FROM Coins ORDER BY coin_id;')
            all = cursor.fetchall()
            cursor.close()
            return all
        except:
            raise SearchError

    def amount_of_coins(self):
        """
        Returns the total amount of coins in the database.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT coin_id FROM Coins;')
            output = cursor.fetchall()
            cursor.close()
            amount = 0
            for val in output:
                amount += 1
            return amount
        except:
            raise SearchError

    def by_type(self):
        """
        Returns how many coins of each type are in the database.
        """
        try:
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
        except:
            raise SearchError

    def by_mint(self):
        """
        Returns the amount of coins minted in each location.
        """
        try:
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
        except:
            raise SearchError

    def total_val(self):
        """
        Returns the overall value of all coins in your database.
        """
        try:
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
        except:
            raise SearchError

    def most_expensive(self):
        """
        Returns the value of the most expensive coin in the database.
        """
        try:
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
        except:
            raise SearchError

    def oldest_coin(self):
        """
        Returns the year of the oldest coin in the database.
        """
        try:
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
        except:
            raise SearchError

if __name__ == "__main__":
    db = database("Coin")
    user = input("Username: ")
    passwrd = input("Password: ")
    host = input("Host: ")
    db.login(user, passwrd, host)
    db.remove('abasj')
    db.quit()
