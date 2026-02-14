import logging
import threading
import time
import concurrent.futures
import random

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


def multiThreadtest():
    threads = list()
    for index in range(3):
        logging.info("Main  : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()
    
    for index, thread in enumerate(threads):
        logging.info("Main  : before joing the thread %d.", index)
        thread.join()
        logging.info("Main : thread %d done", index)
    logging.info("Main  : all done")
    


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

#     logging.info("Main  : before creating thread")
#     x = threading.Thread(target=thread_function, args=(1,))
#     logging.info("Main  : before running thread")
#     x.start()
#     logging.info("Main  : wait for thread to finish")
#     x.join()
#     logging.info("Main  : all done")

def WithConcurrent():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()
    
    def update(self, name):
        logging.info("Thread %s: starting update", name)
        with self._lock:
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
        logging.info("Thread %s: finishing update", name)

def RaceCond():
    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Testing update. Ending value is %d.", database.value)

#-------------------------------------------
# Prodducer consumer

class Pipeline:
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()

    def get_message(self, name):
        logging.debug("%s:about to acquire getlock", name)
        self.consumer_lock.acquire()
        message = self.message
        self.producer_lock.release()
        logging.debug("%s:setlock released", name)
        return message
    
    def set_message(self, message, name):
        logging.debug("%s:about to acquire setlock", name)
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()
        logging.debug("%s:getlock released", name)



SENTINEL = object()

def producer(pipeline):
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")

    pipeline.set_message(SENTINEL, "Producer")

def consumer(pipeline):
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: %s", message)


def producerConsumerTest():
    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # WithConcurrent()
    # RaceCond()
    producerConsumerTest()

    
    