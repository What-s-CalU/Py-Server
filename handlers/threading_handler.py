from threading import Lock

s_print_lock        = Lock()
update_message_lock = Lock()

NOTIFICATION_MESSAGE = "No new notifications..."
NOTIFICATION_COUNT   = 0
NOTIFICATION_CODE    = 200
# Generic function for printing in threads (shifts focus for safety purposes, uses locks)
def s_print(*a, **b):
    s_print_lock.acquire()
    print(*a, **b)
    s_print_lock.release()

def update_notifications(message: str, code: int, increment: bool):
    update_message_lock.aquire()
    # block messages whenever a fatal error occured.
    if(NOTIFICATION_CODE < 430):
        NOTIFICATION_MESSAGE = message
        NOTIFICATION_CODE    = code
        if(increment > 0):
            NOTIFICATION_COUNT += 1
    update_message_lock.release()