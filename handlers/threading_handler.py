from threading import Lock

s_print_lock = Lock()

# Generic function for printing in threads (shifts focus for safety purposes, uses locks)
def s_print(*a, **b):
    s_print_lock.acquire()
    print(*a, **b)
    s_print_lock.release()