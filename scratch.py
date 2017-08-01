import queue
import threading
num_worker_threads = 1
done = []
def do_work(item):
    print ("completed",item)

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()
        done.append(item)

q = queue.Queue()
threads = []

for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(1000):
    q.put(item)


while True:
    x = int(input())
    q.put(x)
    if x in done:
        print ("returned after complete",x)
        