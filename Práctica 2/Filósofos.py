#https://www.youtube.com/watch?v=OoMkQKlcOoA
import threading
import time
import sys

class Semaphore(object):

    def __init__(self, initial):
        self.value = initial
        self.lock = threading.Condition(threading.Lock()) #Crea un objeto Condition que utiliza un Lock para manejar la sincronización.
        #Permite que uno o mas hilos esperen hasta que se de cierta condicion


    def up(self): #libera palillo
        with self.lock: #with me asegura que un fil[osofo aceda a la vez (recurso compartido)
            self.value += 1 #valor del semaforo
            self.lock.notify() # bloquee recuro y llamo para que acceda


    def down(self): #toma palillo
        with self.lock: #asegura sincronizacion
            while self.value==0: #no hay recursos disponibles--> el semaforo marca 0
                self.lock.wait() #hago esperar al resto
        self.value -=1 #indico que libero palillo


class Chopstick(object):
    def __init__(self, number):
        self.number = number #id palillo
        self.user = -1 #filosofo que lo usa
        self.lock = threading.Condition(threading.Lock())
        self.taken=False

    def take(self, user):
        with self.lock:
            while self.taken==True:
                self.lock.wait()
        self.user=user
        self.taken=True
        sys.stdout.write("Filósofo[%s] toma el palillo:%s\n" % (user, self.number))
        self.lock.notifyAll()

    def drop(self, user):
        with self.lock:
            while self.taken==False:
                self.lock.wait()
            self.user = user
            self.taken = False
            sys.stdout.write("Filósofo[%s] toma el palillo:%s\n" % (user, self.number))
            self.lock.notifyAll()
class Philosopher(threading.Thread):

    def __init__(self, left, right, number, butler):
        threading.Thread.__init__(self)
        self.number =number #para identidficar el filosofo
        self.left = left
        self.right = right
        self.butler = butler

    def run(self):
        for i in range(1):
            self.butler.down()
            print("Filosofo", self.number, "piensa")
            time.sleep(0.1)
            self.left.take(self.number) #el numero es el usuario
            time.sleep(0.1)
            self.right.take(self.number)
            print("Filosofo", self.number, "come")
            time.sleep(0.1)
            self.right.drop(self.number)
            self.left.drop(self.number)
            self.butler.up() #termina el servicio
        sys.stdout.write("Filósofo[%s] toma el palillo:%s\n" % self.number)