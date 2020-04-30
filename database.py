import mysql.connector
from mysql.connector import errorcode

class Database():

    def __init__(self):
        self.connect()

    def printError(self, e):
        print("SOMETHING WENT WRONG: {}".format(e))

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "0p3nm35H",
                database = "TWITCHBOT",
                auth_plugin="mysql_native_password"
            )
            self.crsr = self.db.cursor()
        except mysql.connector.Error as e:
            self.printError(e)
            self.db = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "0p3nm35H",
                auth_plugin="mysql_native_password"
            )
            self.crsr = self.db.cursor()
            self.execute("CREATE DATABASE TWITCHBOT;")
            self.execute("USE TWITCHBOT;")

        self.commit()

    def execute(self, s):
        try:
            self.crsr.execute(s)
        except mysql.connector.Error as e:
            self.printError(e)

    def commit(self):
        try:
            self.db.commit()
        except mysql.connector.Error as e:
            self.printError(e)

    def createTable(self, n, c, p):
        cols = ", ".join(c)
        com = "CREATE TABLE " + n + " (" + cols + ", PRIMARY KEY (" + p + "));"
        self.execute(com)
        self.commit()

    def createLinkedTable(self, n, c, p, f, t):
        cols = ", ".join(c)
        com = "CREATE TABLE " + n + " (" + cols + ", PRIMARY KEY (" + p + "), FOREIGN KEY(" + f + ") REFERENCES " + t + "(" + f + "));"
        self.execute(com)
        self.commit()

    def dataInsert(self, n, c, v):
        cols = ", ".join(c)
        vals = "', '".join(v)
        self.execute("INSERT INTO " + n + " (" + cols + ") VALUES ('" + vals + "');")
        self.commit()

    def trim(self, s):
        s = s.replace('(\'', '')
        s = s.replace('\',)', '')
        return s

    def dataPull(self, n, t, c, v):
        com = "SELECT " + n + " FROM " + t + " WHERE " + c + "='" + v + "';"
        self.execute(com)
        found = str(self.crsr.fetchone())
        self.cleanup()
        return self.trim(found)

    def rolePull(self, s, n):
        com = "SELECT roleID FROM dRoles WHERE serverID='" + s + "' AND name='" + n + "';"
        self.execute(com)
        found = str(self.crsr.fetchone())
        self.cleanup()
        return self.trim(found)

    def cleanUp(self):
        try:
            self.crsr.nextset()
            self.crsr.close()
            self.db.close()
            self.connect()
        except mysql.connector.Error as e:
            self.printError(e)
