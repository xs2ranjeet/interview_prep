'''
Multi-threaded Fizzbuzz problem
- print num from 1 to N
- for multiple of 3, print Fizz
- for "           5, print Buzz
- for multiple of 3 and 5, print FizzBuzz
'''

import threading

MAX_NUM = 50
counter = 1
lock = threading.Lock()

def print_fizzbuzz_or_num(thread_id):
    global counter
    while counter < MAX_NUM:
        with lock:
            if counter > MAX_NUM:
                return
            if counter % 3  == 0 and counter % 5 == 0:
                print(f"Thread: {thread_id + 1} : FizzBuzz")
            elif counter % 3 == 0:
                print(f"Thread: {thread_id + 1} : Fizz")
            elif counter % 5 == 0:
                print(f"Thread: {thread_id + 1} : Buzz")
            else:
                print(f"Thread: {thread_id + 1} : {counter}")
            counter += 1

# condition = threading.Condition(lock)
# def fizz(thread_id, num):
#     with condition:
#         while num % 3 != 0:
#             condition.wait()
#         print(f"Thread: {thread_id} -> Fizz")
#         condition.notify_all()

# def buzz(thread_id, num):
#     with condition:
#         while num % 5 != 0:
#             condition.wait()
#         print(f"Thread: {thread_id} -> Buzz")
#         condition.notify_all()

# def fizzbuzz(thread_id, num):
#     with condition:
#         while num % 3 != 0 and num % 5 != 0:
#             condition.wait()
#         print(f"Thread: {thread_id} -> FizzBuzz")
#         condition.notify_all()

# def number(thread_id, num):
#     with condition:
#         while num % 3 == 0 or num % 5 == 0:
#             condition.wait()
#         print(f"Thread: {thread_id} -> {num}")
#         condition.notify_all()

# threads = list()
# for index in range(3):
#     t = threading.Thread(target = print_fizzbuzz_or_num, args=(index,))
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.curr = 1
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        while True:
            with self.condition:
                while self.curr <= self.n and not(self.curr % 5 != 0 and self.curr % 3 == 0):
                    self.condition.wait()
                if self.curr > self.n:
                    return
                
                printFizz()
                self.curr += 1
                self.condition.notify_all()
            

    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
         while True:
            with self.condition:
                while self.curr <= self.n and not(self.curr % 5 == 0 and self.curr % 3 != 0):
                    self.condition.wait()
                if self.curr > self.n:
                    return
                
                printBuzz()
                self.curr += 1
                self.condition.notify_all()
    
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
         while True:
            with self.condition:
                while self.curr <= self.n and not(self.curr % 15 == 0):
                    self.condition.wait()
                if self.curr > self.n:
                    return
                
                printFizzBuzz()
                self.curr += 1
                self.condition.notify_all()
    
    def number(self, printNum: 'Callable[[int], None]') -> None:
         while True:
            with self.condition:
                while self.curr <= self.n and (self.curr % 5 == 0 or self.curr % 3 == 0):
                    self.condition.wait()
                if self.curr > self.n:
                    return
                
                printNum(self.curr)
                self.curr += 1
                self.condition.notify_all()

def printFizz():
    print("fizz")

def printBuzz():
    print("buzz")

def printFizzBuzz():
    print("fizzbuzz")

def printNumber(x):
    print(x)
 
if __name__ == "__main__":
    n = 20
    fizzbuzz = FizzBuzz(n)
    t1 = threading.Thread(target=fizzbuzz.fizz, args=(printFizz,))
    t2 = threading.Thread(target=fizzbuzz.buzz, args=(printBuzz,))
    t3 = threading.Thread(target=fizzbuzz.fizzbuzz, args=(printFizzBuzz,))
    t4 = threading.Thread(target=fizzbuzz.number, args=(printNumber,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()