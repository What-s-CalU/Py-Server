'''
    Interfacing functions for GPIO and other pi-exclusive features. 
    "test program for interfacing a 16x2 Display with LEDs and buttons "
'''

#! /usr/bin/env python


from time import sleep
import threading
import RPi.GPIO as rasp_io
import drivers
import handlers.threading_handler as thread_h
import global_values as glob

# globals specific to this module. 
PIN_BTN_1: int = 17
PIN_BTN_2: int = 27
PIN_LED_1: int = 4
PIN_LED_2: int = 22


# for long string Parameters:
# (driver, string to print, number of line to print, number of columns of your display) 
#Return: This function send to display your scrolling string.
def long_string(display, text="", num_line=1, num_cols=16):
    try:
        if len(text) > num_cols:
            display.lcd_display_string(text[:num_cols], num_line)
            sleep(1)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i+num_cols]
                display.lcd_display_string(text_to_print, num_line)
                sleep(1)
            sleep(1)
        else:
            display.lcd_display_string(text, num_line)
    except Exception as e:
        print("Error in long_string():", e)
        pass  # Pass and do nothing if there is an error


# Hardware's tasks as a thread, intended to run forever. 
class CALUHardwareManagerThread(threading.Thread):
       def run(self):

            # mode and warning flags. 
            rasp_io.setmode(rasp_io.BCM)
            rasp_io.setwarnings(False)

            # Load the driver and set it to "display"
            display = drivers.Lcd() 

            #GPIO connections 
            #################################################################
            # set up for first led pin and it's button. 
            rasp_io.setup (PIN_LED_1, rasp_io.OUT)
            rasp_io.setup (PIN_BTN_1, rasp_io.IN, pull_up_down=rasp_io.PUD_UP)
            rasp_io.output(PIN_LED_1, False)


            # set up for second led pin and it's button. 
            rasp_io.setup (PIN_LED_2,rasp_io.OUT)
            rasp_io.setup (PIN_BTN_2,rasp_io.IN, pull_up_down=rasp_io.PUD_UP)
            rasp_io.output(PIN_LED_2,False)
            #################################################################



            # GPIO events
            ####################################################################
            # inline functions for buttons 1 and 2
            def pin_btn_callback(channel):
                if(glob.BUTTON_SUPPRESS):
                    glob.BUTTON_SUPPRESS = False
                else:
                    thread_h.update_message_lock.acquire()
                    glob.NOTIFICATION_FOCUSED_MESSAGE = glob.NOTIFICATION_MESSAGE
                    thread_h.update_message_lock.release()
                    glob.BUTTON_SUPPRESS = True
                rasp_io.output(PIN_LED_1, True)
                sleep(1)
                rasp_io.output(PIN_LED_1,False)


            def pin_btn_callback_clear(channel):
                rasp_io.output(PIN_LED_2, True)
                sleep(1)
                rasp_io.output(PIN_LED_2, False)
                display.lcd_clear()
                display.lcd_display_string("clearing ...", 1) 
                display.lcd_display_string("screen   ...", 2)
                display.lcd_clear()
                thread_h.update_notifications("No new notifications...", 200, True)
                sleep(2)
                display.lcd_clear()
                sleep(2)
            ####################################################################

            
            # binds functions to buttons 1 and 2
            rasp_io.add_event_detect(PIN_BTN_1, rasp_io.FALLING, callback=pin_btn_callback,       bouncetime=200)
            rasp_io.add_event_detect(PIN_BTN_2, rasp_io.FALLING, callback=pin_btn_callback_clear, bouncetime=200)


            #continous loop for LCD display
            #######################################################################
            
            display.lcd_display_string("What's @ CALU!", 1)  # Write line of text to first line of display
            sleep(3)
            try:
                while True:
                    if(glob.BUTTON_SUPPRESS):
                        long_string(display, glob.NOTIFICATION_FOCUSED_MESSAGE, 2)
                        sleep(2)
                        display.lcd_clear()
                    else:
                        display.lcd_display_string("Notifications:", 1)
                        # try to acquire the new global notification string
                        thread_h.update_message_lock.acquire()
                        long_string(display, glob.NOTIFICATION_MESSAGE, 2)
                        thread_h.update_message_lock.release()
                        sleep(2)
                        display.lcd_clear()
            except KeyboardInterrupt as e:
                print(e)
                display.lcd_clear()	 # clear the display 
                rasp_io.cleanup()	 # clear gpio settings 
            ######################################################################
