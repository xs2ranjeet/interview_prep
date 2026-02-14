import threading
import time

lock = threading.Lock()
condition = threading.Condition(lock)
MAX_NUMBER = 100
current_num = 1
turn = 0
MAX_THREAD = 3
def worker(id):
    global current_num, turn
    while True:
        with condition:
            while turn != id:
                condition.wait()
            if current_num > MAX_NUMBER:
                condition.notify_all()
                return
            
            print(f'Worker {id + 1}: {current_num}')
            current_num += 1
            turn = (turn + 1) % (MAX_THREAD)
            condition.notify_all()

threads = []
for i in range(MAX_THREAD):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()