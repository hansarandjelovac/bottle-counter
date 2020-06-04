import mysql.connector
import time
import os


def backupBaze():

    os.system('mysqldump -uroot -pubiquiti proba > /home/pi/bottle-counter/beta/backup/baza_$(date "+%b_%d_%Y_%H_%M_%S").sql')

def brisanjeTabele():
    
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="ubiquiti",
        database="proba"
    )
    
    print ("Konekcija sa bazom uspostavljena")
    time.sleep(2)
    

    mycursor = mydb.cursor()

    sql = "TRUNCATE TABLE test"
    mycursor.execute(sql)
    mydb.commit()
    
    print ("Podaci iz baze 'test' su obrisani")
    time.sleep(2)
        
    mycursor = mydb.cursor()

    sql = "INSERT INTO test (idSenzora, idRaf, idRed, IdKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (1,1,1,1,1,0,0,0)"
    mycursor.execute(sql)
    mydb.commit()
    
    print ("Inicijalizovan senzor broj 1")
    time.sleep(2)
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO test (idSenzora, idRaf, idRed, IdKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (2,1,1,2,1,0,0,0)"
    mycursor.execute(sql)
    mydb.commit()
    
    print ("Inicijalizovan senzor broj 2")
    time.sleep(2)
    
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO test (idSenzora, idRaf, idRed, IdKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (3,1,1,3,1,0,0,0)"
    mycursor.execute(sql)
    mydb.commit()
    
    print ("Inicijalizovan senzor broj 3")
    time.sleep(2)
        
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO test (idSenzora, idRaf, idRed, IdKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (4,1,1,4,1,0,0,0)"
    mycursor.execute(sql)
    mydb.commit()
    
    print ("Inicijalizovan senzor broj 4")
    time.sleep(2)
    
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO test (idSenzora, idRaf, idRed, IdKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (5,1,1,5,1,0,0,0)"
    mycursor.execute(sql)
    mydb.commit()
    
    print ("Inicijalizovan senzor broj 5")
    time.sleep(2)

backupBaze()
brisanjeTabele()

