import time
import mysql.connector
import functools
import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER1 = 15
GPIO_ECHO1 = 23
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO_TRIGGER2 = 20
GPIO_ECHO2 = 21
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

global velicinaPushera
velicinaPushera = 50

# inicijalna konekcija na bazu
def mySqlConnect():
    global mydb
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="ubiquiti",
        database="proba"
    )
    
#PRECNIK AMBALAZE PRVOG SENZORA
def velicinaAmbalaze1():
       
    mycursor = mydb.cursor()
    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 1 ;")
    x = mycursor.fetchone()
    x = functools.reduce(lambda sub, ele: sub * 10 + ele, x)
    print (x)
    
    sql = "SELECT precnikAmbalaze FROM proizvodi WHERE id = %s" %x
    mycursor.execute(sql)
    global precnik1
    precnik1 = mycursor.fetchone()
    precnik1 = functools.reduce(lambda sub, ele: sub * 10 + ele, precnik1) 
    print (precnik1, "cm")
    
    
#CITANJE ID IZ DRUGE TABELE (koji je proizvod na senzoru)  
def citanjeId1():
    #mysqlconnect()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 1 ;")
    global idProizvod1
    idProizvod1 = mycursor.fetchone()
    idProizvod1 = functools.reduce(lambda sub, ele: sub * 10 + ele, idProizvod1)
    
    
#iscitavanje koliko moze da stane u raf za prvi senzor
# OVDE TREBA NAPRAVITI DA SE UBACUJE U TABELU TAKO STO CES DUZINU PUSHERA PODELITI SA PRECNIKOM AMBALAZE
def kolikoStajeURaf1():
    
    mycursor = mydb.cursor()
    global kolikoStajeURaf1
    kolikoStajeURaf1 = velicinaPushera / precnik1
    sql = "UPDATE rasporedProizvoda SET kolikoStajeURaf=%s WHERE id=1;" %kolikoStajeURaf1
    mycursor.execute(sql)
    mydb.commit()
    print ("U raf staje", kolikoStajeURaf1)
            
#merenje distance za prvi senzor

def rastojanje1():
    
    GPIO.output(GPIO_TRIGGER1, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance1 = (TimeElapsed * 34300) / 2
 
    print ("distanca je", distance1)
    return distance1    
    
    
    
# citanje poslednje kolicine iz baze za prvi senzor zbog uporedjivanja sa trenutnim stanjem

def citanjeIzBaze1():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT trenutnoStanje FROM test WHERE idSenzora = 1 ORDER BY id DESC LIMIT 1;")
    
    global trenutnaKolicinaUBazi1
    trenutnaKolicinaUBazi1 = mycursor.fetchone()
    print (trenutnaKolicinaUBazi1)

    #konvertovanje tuple u int
    trenutnaKolicinaUBazi1 = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicinaUBazi1)
    return trenutnaKolicinaUBazi1    


# merenje trenutne kolicine za prvi senzor
def merenjeKolicine1():

    dist = int(rastojanje1())
    print ("distanca PRVOG senzora",dist)
    
    global kolicina1
    
    kolicina1 = (velicinaPushera - dist) // precnik1
    kolicina1 = int(kolicina1)
    print ("KOLICINA", kolicina1)
    
       
    
    
        
#uporedjivanje stanja i upisivanje u tabelu trecu        
def uporedjivanjeStanja():
    
    if trenutnaKolicinaUBazi1 > kolicina1:
        uzetoIzRafa1 = trenutnaKolicinaUBazi1 - kolicina1

    else:
        uzetoIzRafa1 = 0

    if trenutnaKolicinaUBazi1 < kolicina1:
        dodatoURaf1 = kolicina1 - trenutnaKolicinaUBazi1

    else:
        dodatoURaf1 = 0


    if  kolicina1 == trenutnaKolicinaUBazi1:
        pass
        print ("nema promena PRVOG senzora\n")

    else:

        mycursor = mydb.cursor()

        sql = "INSERT INTO test (idSenzora, idRaf, idRed, idKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = ("1", "1", "1", "1", idProizvod1, kolicina1, dodatoURaf1, uzetoIzRafa1)
        mycursor.execute(sql, val)

        mydb.commit()

        print ("upisana nova kolicina PRVOG senzora\n", kolicina1)

    
    
mySqlConnect()    
velicinaAmbalaze1()   
citanjeId1()
kolikoStajeURaf1()
rastojanje1()
citanjeIzBaze1()
merenjeKolicine1()
uporedjivanjeStanja()
