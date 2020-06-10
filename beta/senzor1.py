#!/usr/bin/env python
import time
import mysql.connector
import functools
import RPi.GPIO as GPIO
import math
import datetime


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 15
ECHO = 23
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)



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
    mycursor.execute("SELECT velicina FROM rasporedProizvoda WHERE id = 1 ;")
    global velicinaPushera
    velicinaPushera = mycursor.fetchone()
    velicinaPushera = functools.reduce(lambda sub, ele: sub * 10 + ele, velicinaPushera)
    print (velicinaPushera," pusher")


#PRECNIK AMBALAZE PRVOG SENZORA
def velicinaAmbalaze1():
       
    mycursor = mydb.cursor()
    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 1 ;")
    x = mycursor.fetchone()
    x = functools.reduce(lambda sub, ele: sub * 10 + ele, x)
    #print (x)
    
    sql = "SELECT precnikAmbalaze FROM proizvodi WHERE id = %s" %x
    mycursor.execute(sql)
    global precnik1
    precnik1 = mycursor.fetchone()
    precnik1 = functools.reduce(lambda sub, ele: sub * 10 + ele, precnik1) 
    print (precnik1, "cm")
    print("BAG", velicinaPushera, precnik1)
    
    
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
def kolikoStajeURaf():
    
    mycursor = mydb.cursor()
    global kolikoStajeURaf1
    print("BAG", velicinaPushera + precnik1)
    kolikoStajeURaf1 = velicinaPushera / precnik1
    kolikoStajeURaf1 = round(kolikoStajeURaf1)
    sql = "UPDATE rasporedProizvoda SET kolikoStajeURaf=%s WHERE id=1;" %kolikoStajeURaf1
    mycursor.execute(sql)
    mydb.commit()
    print ("U raf staje", kolikoStajeURaf1)
            
#merenje distance za prvi senzor

def rastojanje():
    
    try:
        maxTime = 0.04
    
        while True:
    
            GPIO.output(TRIG,False)
    
            time.sleep(0.01)
    
            GPIO.output(TRIG,True)
    
            time.sleep(0.00001)
    
            GPIO.output(TRIG,False)
    
            pulse_start = time.time()
            timeout = pulse_start + maxTime
            while GPIO.input(ECHO) == 0 and pulse_start < timeout:
                pulse_start = time.time()
    
            pulse_end = time.time()
            timeout = pulse_end + maxTime
            while GPIO.input(ECHO) == 1 and pulse_end < timeout:
                pulse_end = time.time()
    
            pulse_duration = pulse_end - pulse_start
            global distance0
            distance0 = pulse_duration * 17000
            return distance0
    except:
        GPIO.cleanup()

 
def merenja():
    
    distance2 = rastojanje()
    #print("merenje 1", distance2)
    time.sleep(0.3)
    distance3 = rastojanje()
    #print ("merenje 2", distance3)
    time.sleep(0.3)
    distance4 = rastojanje()
    #print("merenje 1", distance4)
    time.sleep(0.3)
    distance5 = rastojanje()
    #print ("merenje 2", distance5)
    time.sleep(0.3)
    distance6 = rastojanje()
    #print("merenje 1", distance6)
    time.sleep(0.3)
    distance7 = rastojanje()
    #print ("merenje 2", distance7)
    time.sleep(0.3)
    distance8 = rastojanje()
    #print("merenje 1", distance8)
    time.sleep(0.3)
    distance9 = rastojanje()
    #print ("merenje 2", distance9)
    time.sleep(0.3)
    distance10 = rastojanje()
    #print ("merenje 2", distance10)
    
     ########################################################
     
    #global distance1
    #minimum = min(distance0, distance2, distance3, distance4, distance5, distance6, distance7, distance8, distance9, distance10)
    #maksimum = max(distance0, distance2, distance3, distance4, distance5, distance6, distance7, distance8, distance9, distance10)
   #distance1 = ((distance0 + distance2+distance3+distance4+distance5+distance6+distance7+distance8+distance9+distance10 - minimum - maksimum) /8 )
    #print ("Srednja vrednost je", distance1)
    
    global distance1
    lista = [distance0, distance2, distance3, distance4, distance5, distance6, distance7, distance8, distance9, distance10]
    #print lista
    minimum3 = sorted(lista) [:3]
    maximum3 = sorted(lista, reverse = True) [:3]
    #print ("MAKSIMUM", maximum3)
    #print ("MINIMUM", minimum3)
    distance1 = ((sum(lista) - sum(minimum3) - sum(maximum3)) / 4)
    print ("Srednja vrednost je", distance1)
        
# citanje poslednje kolicine iz baze za prvi senzor zbog uporedjivanja sa trenutnim stanjem

def citanjeIzBaze1():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT trenutnoStanje FROM test WHERE idSenzora = 1 ORDER BY id DESC LIMIT 1;")
    
    global trenutnaKolicinaUBazi1
    trenutnaKolicinaUBazi1 = mycursor.fetchone()
    #print (trenutnaKolicinaUBazi1)

    #konvertovanje tuple u int
    trenutnaKolicinaUBazi1 = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicinaUBazi1)
    return trenutnaKolicinaUBazi1    


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
        print ("nema promena PRVOG senzora\n")
        print ("----------------------------------------------------------")

    else:

        mycursor = mydb.cursor()

        sql = "INSERT INTO test (idSenzora, idRaf, idRed, idKolona, idProizvod, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = ("1", "1", "1", "1", idProizvod1, kolicina1, dodatoURaf1, uzetoIzRafa1)
        mycursor.execute(sql, val)

        mydb.commit()
        
        #SPLASH SLIKA UZETOG PROIZVODA
        f = open("/var/www/html/php/splash.txt", "w")
        now = datetime.datetime.now()
        vreme = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write("IDProizvod/1|Red/1|Kolona/1|Uzeto/1|Dodato/0|Datum/%s" % vreme)
        f.close()

        print ("upisana nova kolicina PRVOG senzora\n", kolicina1)
        print ("----------------------------------------------------------")

    
while True:
    
    mySqlConnect()  
    dinamickaVelicinaPushera()  
    velicinaAmbalaze1()   
    citanjeId1()
    kolikoStajeURaf()
    rastojanje()
    merenja()
   ## time.sleep(3)
    citanjeIzBaze1()
    merenjeKolicine1()
    uporedjivanjeStanja()
    time.sleep(20)
