from threading import Lock
import global_values            as glob

s_print_lock        = Lock()
update_message_lock = Lock()

# Generic function for printing in threads (shifts focus for safety purposes, uses locks)
def s_print(*a, **b):
    s_print_lock.acquire()
    print(*a, **b)
    s_print_lock.release()

def update_notifications(message: str, code: int, increment: bool):
    update_message_lock.acquire()
    # block messages whenever a fatal error occured.
    if(glob.NOTIFICATION_CODE < 410):
        glob.NOTIFICATION_MESSAGE = message
        glob.NOTIFICATION_CODE    = code
        if(increment > 0):
            glob.NOTIFICATION_COUNT += 1
    update_message_lock.release()