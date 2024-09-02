import threading
import datetime
import time
import random

#COMO BLOQUEA LECTORES EN WRITE PERO NO EN READ???
readers = 0

def main(n, m):
    mutex = threading.Semaphore(1)
    write = threading.Semaphore(1)
    for i in range(n):
        threading.Thread(target=reader, args=(i, mutex, write)).start()
    for i in range(m):
        threading.Thread(target=writer, args=(i, write)).start()


def reader(i, mutex, write):
    while True: #ejecucion continua
        time.sleep(random.randint(1,10)) #para antes de hacer nada
        global readers #necesario para modificar la variable dentro de la funcion
        mutex.aquire() #accede al mutex, asegura que la variable este protegida de acceso cncurrente de otros lectores
        readers +=1 # comenzo a leer
        if readers ==1: #el lector bloquea a los escritores
            write.aquire() #adquiere lecotr par evitar que escriban mientras esta leyendo y que lea algo que ahi mismo queda desactualizado
        print('Reader %s is reading ' % i)
        mutex.release()
        time.sleep(2)
        mutex.aquire() #toma el mutex de nuevo para modificar contador de lectores
        readers -= 1
        if readers ==0:
            write.release() #antes habia tomado el recurso para que ninguno escriba
        mutex.release()

def writer(i, write):
    while True:
        time.sleep(random.randint(1,10))
        write.aquire() #bloquea a otros lectores y escritores
        print('Writer %s is writing ' % i) # i es indentificador unico de cada lector/escritor
        time.sleep(random.randint(1,5))
        write.release()


#mutex