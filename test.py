import time
import mysql.connector
import functools
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO_TRIGGER_1 = 20
GPIO_ECHO_1 = 21
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)



def mySqlConnect():
    global mydb
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="ubiquiti",
        database="proba"
    )
    
    
def velicinaAmbalaze():
    
    #"?|
    

def citanjeId():
    #mysqlconnect()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 1 ;")
    global idProizvod
    idProizvod = mycursor.fetchone()
    idProizvod = functools.reduce(lambda sub, ele: sub * 10 + ele, idProizvod)
    
    mycursor.execute("SELECT idProizvod FROM rasporedProizvoda WHERE id = 2 ;")
    global idProizvod1
    idProizvod1 = mycursor.fetchone()
    idProizvod1 = functools.reduce(lambda sub, ele: sub * 10 + ele, idProizvod1)
    
    #iscitavanje koliko moze da stane proizvoda u raf
    
    mycursor.execute("SELECT kolikoStajeURaf FROM rasporedProizvoda WHERE id = 1 ;")
    global kolikoStajeURaf
    kolikoStajeURaf = mycursor.fetchone()
    kolikoStajeURaf = functools.reduce(lambda sub, ele: sub * 10 + ele, kolikoStajeURaf)
    
    mycursor.execute("SELECT kolikoStajeURaf FROM rasporedProizvoda WHERE id = 2 ;")
    global kolikoStajeURaf1
    kolikoStajeURaf1 = mycursor.fetchone()
    kolikoStajeURaf1 = functools.reduce(lambda sub, ele: sub * 10 + ele, kolikoStajeURaf1)
    
   
    print ("ID prvog senzora je", idProizvod)
    print ("ID drugog senzora je", idProizvod1, "\n")
    
   
   
def rastojanje():
    
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance



#//////////////citanje trenutne kolicine iz baze
def citanjeIzBaze():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT trenutnoStanje FROM test WHERE idProizvod = 1 ORDER BY id DESC LIMIT 1;")
    
    global trenutnaKolicina
    trenutnaKolicina = mycursor.fetchone()
    print (trenutnaKolicina)

    #konvertovanje tuple u int
    trenutnaKolicina = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicina)
    return trenutnaKolicina


#//////
def merenjeKolicine():

    dist = int(rastojanje())
    print ("distanca PRVOG senzora",dist)
    global kolicina

    if dist <=5 :
        kolicina = 3
        print ("kolicina PRVOG senzora",kolicina)
       
    if dist > 5 and dist < 10 :
        kolicina = 2
        print ("kolicina PRVOG senzora",kolicina)

    if dist >= 10 :
        kolicina = 1
        print ("kolicina PRVOG senzora",kolicina)


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




def rastojanje1():
    
    GPIO.output(GPIO_TRIGGER_1, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    
    while GPIO.input(GPIO_ECHO_1) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO_1) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance1 = (TimeElapsed * 34300) / 2
 
    return distance1
 

def citanjeIzBaze1():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT trenutnoStanje FROM test WHERE idProizvod = 2 ORDER BY id DESC LIMIT 1;")

    global trenutnaKolicina1
    trenutnaKolicina1 = mycursor.fetchone()

    #konvertovanje tuple u int
    trenutnaKolicina1 = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicina1)
    return trenutnaKolicina1


def merenjeKolicine1():

    dist1 = int(rastojanje1())
    print ("distanca DRUGOG senzora",dist1)
    global kolicina1

    if dist1 <=5 :
        kolicina1 = 3
        print ("kolicina DRUGOG senzora",kolicina1)
    
    if dist1 > 5 and dist1 < 10 :
        kolicina1 = 2
        print ("kolicina DRUGOG senzora",kolicina1)
        
    if dist1 >= 10 :
        kolicina1 = 1
        print ("kolicina PRVOG senzora",kolicina1)
          

def uporedjivanjeStanja1():
    
    if trenutnaKolicina1 > kolicina1:
        uzetoIzRafa1 = trenutnaKolicina1 - kolicina1

    else:
        uzetoIzRafa1 = 0

    if trenutnaKolicina1 < kolicina1:
        dodatoURaf1 = kolicina1 - trenutnaKolicina1

    else:
        dodatoURaf1 = 0


    if  kolicina1 == trenutnaKolicina1:
        pass
        print ("nema promena DRUGOG senzora\n")

    else:

        mycursor = mydb.cursor()

        sql = "INSERT INTO test (idRaf, idRed, idKolona, idProizvod, kolikoStajeURaf, trenutnoStanje, dodatoURaf, uzetoIzRafa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = ("1", "1", "1", idProizvod1, kolikoStajeURaf1, kolicina1, dodatoURaf1, uzetoIzRafa1)
        mycursor.execute(sql, val)

        mydb.commit()

        print ("upisana nova kolicina DRUGOG senzora\n", kolicina1)


while True:
    mySqlConnect()
    citanjeId()
    time.sleep(2)
    citanjeIzBaze()
    merenjeKolicine()
    uporedjivanjeStanja()
    time.sleep(2)
    citanjeIzBaze1()
    merenjeKolicine1()
    uporedjivanjeStanja1()
    time.sleep(2)