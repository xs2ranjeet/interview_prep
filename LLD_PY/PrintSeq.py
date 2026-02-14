'''
Print Number from 1 to 100: 
- 3 threads
- sequential order:
- thread sync: make sure each thread print one num at a time. and no miss
- No race condition:
'''
import threading

MAX_NUMBER = 100
current_num = 1

lock = threading.Lock()
condition = threading.Condition(lock)
N = 4
# 0 -> Th1, 1-> Th2, 2-> Th3
turn = 0

def print_number_cond(thread_id):
    global current_num, turn

    while True:
        with condition:
            # wait until it is thread's turn
            while turn != thread_id:
                condition.wait()
            
            if current_num > MAX_NUMBER:
                condition.notify_all()
                return
            print(f"Thread-{thread_id + 1} printed: {current_num}")
            current_num += 1

            turn = (turn + 1) % N

            condition.notify_all()


semaphores = [threading.Semaphore(0) for _ in range(N)]
done = False
# First thread start
semaphores[0].release()

def print_numbers_sem(thread_id):
    global current_num, done
    
    while True:
        semaphores[thread_id].acquire()
        with lock:
            if current_num > MAX_NUMBER:
                done = True
        if done:
            semaphores[(thread_id + 1) % N].release()
            return
        with lock:
            print(f"Thread-{thread_id + 1} printed: {current_num}")
            current_num += 1
        semaphores[(thread_id + 1) % N].release()


threads = []

for i in range(N):
    t = threading.Thread(target=print_numbers_sem, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()