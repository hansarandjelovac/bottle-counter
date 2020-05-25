import time
import mysql.connector
import functools
import RPi.GPIO as GPIO

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
velicinaPushera = 80

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
    global idProizvod
    idProizvod = mycursor.fetchone()
    idProizvod = functools.reduce(lambda sub, ele: sub * 10 + ele, idProizvod)
    
    
#iscitavanje koliko moze da stane u raf za prvi senzor
# OVDE TREBA NAPRAVITI DA SE UBACUJE U TABELU TAKO STO CES DUZINU PUSHERA PODELITI SA PRECNIKOM AMBALAZE
def kolikoStajeURaf1():
    
    mycursor = mydb.cursor()
    global x
    x = velicinaPushera / precnik1
    sql = "UPDATE rasporedProizvoda SET kolikoStajeURaf=%s WHERE id=1;" %x
    mycursor.execute(sql)
    mydb.commit()
    print ("U raf staje", x)
            
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
    
    
    
# citanje trenutne kolicine iz baze za prvi senzor

def citanjeIzBaze1():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT trenutnoStanje FROM test WHERE idSenzora = 1 ORDER BY id DESC LIMIT 1;")
    
    global trenutnaKolicina1
    trenutnaKolicina1 = mycursor.fetchone()
    print (trenutnaKolicina1)

    #konvertovanje tuple u int
    trenutnaKolicina1 = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicina1)
    return trenutnaKolicina1    


# merenje trenutne kolicine za prvi senzor
def merenjeKolicine1():

    dist = int(rastojanje1())
    print ("distanca PRVOG senzora",dist)
    
    global kolicina1

    if dist > (velicinaPushera - precnik1) :
        kolicina1 = 0
        print ("kolicina PRVOG senzora",kolicina1)
       
    
    
        
#uporedjivanje stanja i upisivanje u tabelu trecu        
def uporedjivanjeStanja():
    
    if trenutnaKolicina > kolicina:
        uzetoIzRafa = trenutnaKolicina - kolicina

    else:
        uzetoIzRafa = 0

    if trenutnaKolicina < kolicina:
        dodatoURaf = kolicina - trenutnaKolicina

    else:
        dodatoURaf = 0


    if  kolicina == trenutnaKolicina:
        pass
        print ("nema promena PRVOG senzora\n")

    else:

        mycursor = mydb.cursor()

        sql = "INSERT INTO test (idRaf, idRed, idKolona, idProizvod, kolikoStajeURaf, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = ("1", "1", "1", idProizvod, kolikoStajeURaf, kolicina, dodatoURaf, uzetoIzRafa)
        mycursor.execute(sql, val)

        mydb.commit()

        print ("upisana nova kolicina PRVOG senzora\n", kolicina)

    
    
mySqlConnect()    
velicinaAmbalaze1()   
citanjeId1()
kolikoStajeURaf1()
rastojanje1()
citanjeIzBaze1()
merenjeKolicine1()