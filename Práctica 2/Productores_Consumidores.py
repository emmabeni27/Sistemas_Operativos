import threading
import time

buffer = []

def main(n, m, s):
    empty = threading.Semaphore(s)
    full = threading.Semaphore(0)
    mutex = threading.Semaphore(1)

    for i in range(n):
        threading.Thread(target=producer, args=(i, empty, full, mutex)).start()
    for i in range(m):
        threading.Thread(target=consumer, args=(i, empty, full, mutex)).start()

def producer(i, empty, full, mutex):
    while True:
        item = i
        time.sleep(2)
        empty.acquire()
        mutex.acquire()
        buffer.append(item)
        print('Producer %s produced item %s' % (i, item))
        mutex.release()
        full.release()

def consumer(i, empty, full, mutex):
    while True:
        time.sleep(3)
        full.acquire()
        mutex.acquire()
        item = buffer.pop(0)
        print('Consumer %s consumed item %s' % (i, item))
        mutex.release()
        empty.release()

