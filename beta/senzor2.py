#!/usr/bin/python
import time
import mysql.connector
import functools
import RPi.GPIO as GPIO
import math
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER1 = 20
GPIO_ECHO1 = 21
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)



# inicijalna konekcija na bazu
def mySqlConnect():
    global mydb
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="ubiquiti",
        database="proba"
    )
    

def dinamickaVelicinaPushera():
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT velicina FROM rasporedProizvoda WHERE id = 2 ;")
    global velicinaPushera
    velicinaPushera = mycursor.fetchone()
    velicinaPushera = functools.reduce(lambda sub, ele: sub * 10 + ele, velicinaPushera)
    print (velicinaPushera," pusher")
    
#PRECNIK AMBALAZE PRVOG SENZORA
def velicinaAmbalaze1():
       
    mycursor = mydb.cursor()
    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 2 ;")
    x = mycursor.fetchone()
    x = functools.reduce(lambda sub, ele: sub * 10 + ele, x)
    print ("ID iz tabele rasporedPorizvoda je ", x)
    
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

    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 2 ;")
    global idProizvod1
    idProizvod1 = mycursor.fetchone()
    idProizvod1 = functools.reduce(lambda sub, ele: sub * 10 + ele, idProizvod1)
    
    
#iscitavanje koliko moze da stane u raf za prvi senzor
# OVDE TREBA NAPRAVITI DA SE UBACUJE U TABELU TAKO STO CES DUZINU PUSHERA PODELITI SA PRECNIKOM AMBALAZE
def kolikoStajeURaf():
    
    mycursor = mydb.cursor()
    global kolikoStajeURaf1
    kolikoStajeURaf1 = velicinaPushera / precnik1
    kolikoStajeURaf1 = round(kolikoStajeURaf1)
    sql = "UPDATE rasporedProizvoda SET kolikoStajeURaf=%s WHERE id=2;" %kolikoStajeURaf1
    mycursor.execute(sql)
    mydb.commit()
    print ("U raf staje", kolikoStajeURaf1)
            
#merenje distance za prvi senzor

def rastojanje():
    
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
    global distance0
    distance0 = (TimeElapsed * 34300) / 2
    return distance0
 
    
def merenja():
    
    distance2 = rastojanje()
   # print("merenje 1", distance2)
    time.sleep(0.3)
    distance3 = rastojanje()
   # print ("merenje 2", distance3)
    time.sleep(0.3)
    distance4 = rastojanje()
   # print("merenje 1", distance4)
    time.sleep(0.3)
    distance5 = rastojanje()
   # print ("merenje 2", distance5)
    time.sleep(0.3)
    distance6 = rastojanje()
   # print("merenje 1", distance6)
    time.sleep(0.3)
    distance7 = rastojanje()
   # print ("merenje 2", distance7)
    time.sleep(0.3)
    distance8 = rastojanje()
   # print("merenje 1", distance8)
    time.sleep(0.3)
    distance9 = rastojanje()
   # print ("merenje 2", distance9)
    time.sleep(0.3)
    distance10 = rastojanje()
   # print ("merenje 2", distance10)
    
    

    global distance1
    minimum = min(distance0, distance2, distance3, distance4, distance5, distance6, distance7, distance8, distance9, distance10)
    maksimum = max(distance0, distance2, distance3, distance4, distance5, distance6, distance7, distance8, distance9, distance10)
    distance1 = ((distance0 + distance2+distance3+distance4+distance5+distance6+distance7+distance8+distance9+distance10 - minimum - maksimum) /8 )
    print ("Srednja vrednost je", distance1)
   
       
    
    
    
# citanje poslednje kolicine iz baze za prvi senzor zbog uporedjivanja sa trenutnim stanjem

def citanjeIzBaze1():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT trenutnoStanje FROM test WHERE idSenzora = 2 ORDER BY id DESC LIMIT 1;")
    
    global trenutnaKolicinaUBazi1
    trenutnaKolicinaUBazi1 = mycursor.fetchone()
    #print (trenutnaKolicinaUBazi1)

    #konvertovanje tuple u int
    trenutnaKolicinaUBazi1 = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicinaUBazi1)
   # return trenutnaKolicinaUBazi1    


# merenje trenutne kolicine za prvi senzor
def merenjeKolicine1():

    dist = distance1
    print ("distanca PRVOG senzora",dist)
    
    global kolicina1
    
    kolicina1 = (velicinaPushera - dist) / precnik1
    kolicina1 = math.floor(kolicina1)
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
        print ("nema promena drugog senzora\n")
        print ("----------------------------------------------------------")

    else:

        mycursor = mydb.cursor()

        sql = "INSERT INTO test (idSenzora, idRaf, idRed, idKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = ("2", "1", "1", "2", idProizvod1, kolicina1, dodatoURaf1, uzetoIzRafa1)
        mycursor.execute(sql, val)

        mydb.commit()
        
        
       #SPLASH SLIKA UZETOG PROIZVODA
        f = open("/var/www/html/php/splash.txt", "w")
        now = datetime.datetime.now()
        vreme = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write("IDProizvod/1|Red/1|Kolona/2|Uzeto/1|Dodato/0|Datum/%s" % vreme)
        f.close()

       
        print ("upisana nova kolicina drugog senzora\n", kolicina1)
        print ("----------------------------------------------------------")

    
while True:
        
    mySqlConnect()    
    dinamickaVelicinaPushera()
    velicinaAmbalaze1()   
    citanjeId1()
    kolikoStajeURaf()
    rastojanje()
    merenja()
    #time.sleep(3)
    citanjeIzBaze1()
    merenjeKolicine1()
    uporedjivanjeStanja()
    time.sleep(1)