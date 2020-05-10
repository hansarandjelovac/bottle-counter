import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

def citanjeIzBaze():
    
    db= MySQLdb.connect("localhost", "root", "ubiquiti", "proba")

    cursor= db.cursor()

    number_of_rows= cursor.execute("SELECT * FROM test;) 

    for i in range (number_of_rows):
        print (row[i])


    
    
    
while True:
    citanjeIzBaze()
    time.sleep(2)