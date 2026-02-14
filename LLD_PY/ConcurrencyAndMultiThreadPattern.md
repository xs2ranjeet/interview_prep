Below is a **concise LLD-interview friendly guide** to common **Python concurrency patterns**.
Each pattern includes:

* When to use (interview explanation)
* Minimal Python implementation
* Small driver/demo

All examples use **standard library only** (`threading`, `queue`, `concurrent.futures`).

---

# Python Concurrency Patterns for LLD Interviews

---

## 1. Poison Pill Pattern

**Use case:** Graceful shutdown of worker threads.

**Idea:** Send a special object (`None` or sentinel) to signal termination.

```python
import threading
import queue
import time

POISON_PILL = None

def worker(q, wid):
    while True:
        task = q.get()
        if task is POISON_PILL:
            print(f"Worker {wid} shutting down")
            break
        print(f"Worker {wid} processing {task}")
        time.sleep(0.5)
        q.task_done()

def poison_pill_demo():
    q = queue.Queue()
    workers = [threading.Thread(target=worker, args=(q, i)) for i in range(2)]
    for w in workers: w.start()

    for i in range(5):
        q.put(i)

    for _ in workers:
        q.put(POISON_PILL)

    for w in workers: w.join()

poison_pill_demo()
```

---

## 2. Guarded Suspension

**Use case:** Thread waits until condition is met.

```python
import threading

class GuardedQueue:
    def __init__(self):
        self.queue = []
        self.condition = threading.Condition()

    def put(self, item):
        with self.condition:
            self.queue.append(item)
            self.condition.notify()

    def get(self):
        with self.condition:
            while not self.queue:
                self.condition.wait()
            return self.queue.pop(0)

def guarded_demo():
    gq = GuardedQueue()

    def producer():
        for i in range(3):
            print("Producing", i)
            gq.put(i)

    def consumer():
        for _ in range(3):
            print("Consumed", gq.get())

    threading.Thread(target=consumer).start()
    threading.Thread(target=producer).start()

guarded_demo()
```

---

## 3. Double Check Locking (Singleton)

**Use case:** Lazy initialization safely.

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("Creating instance")
                    cls._instance = Singleton()
        return cls._instance

def dcl_demo():
    def task():
        Singleton.get_instance()

    threads = [threading.Thread(target=task) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()

dcl_demo()
```

---

## 4. Balking Pattern

**Use case:** If state not suitable → return immediately.

```python
import threading

class Printer:
    def __init__(self):
        self.lock = threading.Lock()
        self.busy = False

    def print_doc(self, name):
        if self.busy:
            print(f"Balking: Printer busy for {name}")
            return
        with self.lock:
            self.busy = True
            print(f"Printing {name}")
            import time; time.sleep(1)
            self.busy = False

def balking_demo():
    p = Printer()
    for i in range(3):
        threading.Thread(target=p.print_doc, args=(f"Doc-{i}",)).start()

balking_demo()
```

---

## 5. Thread-Safe Storage (Thread-Specific Storage)

**Use case:** Each thread keeps its own data.

```python
import threading

local_data = threading.local()

def process():
    local_data.user = threading.current_thread().name
    print(f"{local_data.user} processing")

def tls_demo():
    threads = [threading.Thread(target=process) for _ in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()

tls_demo()
```

---

## 6. Reader–Writer Lock

**Use case:** Many readers, few writers.

```python
import threading

class RWLock:
    def __init__(self):
        self.readers = 0
        self.lock = threading.Lock()
        self.write_lock = threading.Lock()

    def acquire_read(self):
        with self.lock:
            self.readers += 1
            if self.readers == 1:
                self.write_lock.acquire()

    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release()

    def acquire_write(self):
        self.write_lock.acquire()

    def release_write(self):
        self.write_lock.release()

def rw_demo():
    rw = RWLock()
    data = 0

    def reader():
        rw.acquire_read()
        print("Reading", data)
        rw.release_read()

    def writer():
        nonlocal_data = {'data': 0}
        rw.acquire_write()
        nonlocal_data['data'] += 1
        print("Writing")
        rw.release_write()

rw_demo()
```

(Explain conceptually in interview; Python doesn’t have built-in RWLock.)

---

## 7. Active Object Pattern

**Use case:** Method calls become async tasks via queue.

```python
import threading
import queue

class ActiveObject:
    def __init__(self):
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while True:
            func, args = self.q.get()
            if func is None:
                break
            func(*args)

    def submit(self, func, *args):
        self.q.put((func, args))

    def stop(self):
        self.q.put((None, None))
        self.thread.join()

def active_demo():
    ao = ActiveObject()

    def task(x):
        print("Processing", x)

    for i in range(5):
        ao.submit(task, i)

    ao.stop()

active_demo()
```

---

## 8. Monitor Object Pattern

**Use case:** Object handles its own synchronization.

```python
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

def monitor_demo():
    c = Counter()
    threads = [threading.Thread(target=c.increment) for _ in range(1000)]
    for t in threads: t.start()
    for t in threads: t.join()
    print("Final:", c.value)

monitor_demo()
```

---

## 9. Thread-per-Message Pattern

**Use case:** Each request handled by new thread.

```python
import threading

def handle_request(req):
    print("Handling", req)

def thread_per_message_demo():
    for i in range(5):
        threading.Thread(target=handle_request, args=(i,)).start()

thread_per_message_demo()
```

---

## 10. Barrier Pattern

**Use case:** Threads wait until all reach a point.

```python
import threading
import time

barrier = threading.Barrier(3)

def worker(i):
    print(f"Thread {i} working")
    time.sleep(i)
    print(f"Thread {i} waiting")
    barrier.wait()
    print(f"Thread {i} passed barrier")

def barrier_demo():
    for i in range(3):
        threading.Thread(target=worker, args=(i,)).start()

barrier_demo()
```

---

## 11. Immutable Object Pattern

**Use case:** No locks needed.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    host: str
    port: int

config = Config("localhost", 8080)
```

Interview line: *Immutable objects are inherently thread-safe.*

---

## 12. Asynchronous Pattern (ThreadPool)

```python
from concurrent.futures import ThreadPoolExecutor
import time

def task(x):
    time.sleep(1)
    return x * x

def async_demo():
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task, i) for i in range(5)]
        for f in futures:
            print(f.result())

async_demo()
```

---

## 13. Parallel Processing Pattern

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_task(x):
    return x * x

def parallel_demo():
    with ProcessPoolExecutor() as executor:
        results = executor.map(cpu_task, range(5))
        print(list(results))

parallel_demo()
```

Interview line:

* ThreadPool → I/O bound
* ProcessPool → CPU bound

---

# Quick Interview Summary Table

| Pattern              | Use Case                   |
| -------------------- | -------------------------- |
| Poison Pill          | Graceful shutdown          |
| Guarded Suspension   | Wait for condition         |
| Double Check Locking | Lazy singleton             |
| Balking              | Fail fast if state invalid |
| Thread Local         | Per-thread data            |
| Reader–Writer        | Read-heavy systems         |
| Active Object        | Async method execution     |
| Monitor              | Encapsulated locking       |
| Thread per Message   | Simple request handling    |
| Barrier              | Phase synchronization      |
| Immutable            | Lock-free safety           |
| Async                | Non-blocking tasks         |
| Parallel             | CPU parallelism            |

---

If you want to **prepare for Staff/Agoda level**, I can give next:

* Which patterns are **actually expected in interviews**
* A **single real system** (like SQS / Rate Limiter / Cache) combining 6–7 patterns
* Common **traps interviewers ask** (GIL, race conditions, deadlocks).
