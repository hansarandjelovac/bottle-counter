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



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ubiquiti",
    database="proba"
)

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

    mycursor.execute("SELECT kolicina FROM polica ORDER BY id DESC LIMIT 1;")

    trenutnaKolicina = mycursor.fetchone()

    #konvertovanje tuple u int
    trenutnaKolicina = functools.reduce(lambda sub, ele: sub * 10 + ele, trenutnaKolicina)
    return trenutnaKolicina
#//////
def merenjeKolicine():

    dist = int(rastojanje())
    print ("distanca",dist)
    global kolicina

    if dist <7:
        kolicina = 2
        print ("kolicina",kolicina)
       # return kolicina
    if dist>7:
        kolicina = 1
        print ("kolicina",kolicina)
      #  return kolicina
    
def uporedjivanjeStanja():
    
    if  kolicina == citanjeIzBaze():
        pass
        print ("nema promena\n")

    else:

        mycursor = mydb.cursor()

        sql = "INSERT INTO polica (red, kolicina) VALUES (%s, %s)"
        val = ("1", kolicina)
        mycursor.execute(sql, val)

        mydb.commit()

        print ("upisana nova kolicina\n", kolicina)

while True:
    citanjeIzBaze()
   # print (citanjeIzBaze())
    merenjeKolicine()
    #print (merenjeKolicine())
    uporedjivanjeStanja()
    time.sleep(2)