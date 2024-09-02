import threading
import time
import random
import sys


#AQUIRE Y RELEASE, QUE BLOQUEA CADA UNO???
waiting = 0

def main(n):
    customers = threading.Semaphore(1)
    barber = threading.Semaphore(1)
    mutex = threading.Semaphore(1)
    threading.Thread(target=Barber, args=(barber, customers, mutex)).start()
    for i in range(n):
        threading.Thread(target=Customer, args=(i, barber, customers, mutex)).start()


def Barber(barber, customers, mutex):
    while True:
        customers.aquire() #saber si hay cliente esperando BLOQUEA BARBERO HASTA CLIENTE DISPONIBLE
        mutex.aquire() #toma mutex para modificar waiting
        global waiting
        waiting -= 1
        barber.release()
        print('Barber is cutting hair') #barber.release le indica al cliente que puede sentarse, barbero estaba ocupado y ahora le puede cortar. DESBLOQUEA AL CLIENTE
        mutex.release() #para que otros accedan a waiting
        time.sleep(3)

def Customer(i, barber, customers, mutex):
    global waiting

    time.sleep(random. randint(1,10))
    mutex.aquire()
    if waiting<3:
        waiting += 1
        customers.release() #anuncia que esta esperando
        mutex.release()
        barber.aquire() #BLOQUEA CLIENTE hasta que el barbero lo llame
        print('Customer %s is getting a haircut' %i)
    else:
        print('Customer %s is leaving as no chairs are available' % i)
        mutex.release() #libera mutex pq no puede agregar mas a waiting
