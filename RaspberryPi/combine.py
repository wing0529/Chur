import RPi.GPIO as GPIO
import os
import time
from time import sleep
import RPi_I2C_driver

#!/usr/bin/env python3
# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the button and LED
button_pin = 16  # Common GPIO pin for the button
led_pin = 21

# Set up the button pin as input with pull-down resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Set up the LED pin as output
GPIO.setup(led_pin, GPIO.OUT)

# Set up GPIO for the LCD
lcd = RPi_I2C_driver.lcd(0x3f)

def button_is_pressed():
    return GPIO.input(button_pin) == GPIO.LOW

def wait_for_button_pressed():
    while not button_is_pressed():
        sleep(0.1)

def wait_for_button_release():
    while button_is_pressed():
        sleep(0.1)
        
def wait_for_file(file_path, timeout=50):
    start_time=time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time>timeout:
            raise TimeoutError(f"Timeout waiting for file : {file_path}")
        time.sleep(1)

def display_lcd_with_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()

        lcd.lcd_clear()
        lcd.lcd_display_string("Prediction : ", 1)
        lcd.lcd_display_string(f"{content}", 2)
        sleep(10)

    except Exception as e:
        print(f"Error in display_lcd_with_file: {e}")

output_file_path = 'predicted_judge.txt'

try:
    # LCD Display
    lcd.lcd_clear()
    lcd.lcd_display_string("Device for GRED", 1)
    sleep(5)

    lcd.lcd_clear()
    sleep(1)  # 지워지고 나서 Delay

    lcd.lcd_display_string("Press the button", 1)
    sleep(5)
   
    while True:
        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.HIGH:
            # Turn on the LED
            GPIO.output(led_pin, GPIO.HIGH)

            # Create the filename with the current date and time
            image_filename = "predict.jpg"

            # libcamera-still command
            os.system("libcamera-still --timeout 10000 -o {}".format(image_filename))
           
            # Print the captured image filename
            print(f"Image captured and saved as {image_filename}")

            # Sleep for 0.5 seconds
            time.sleep(0.5)

            lcd.lcd_clear() 
            lcd.lcd_display_string("Measuring...", 1)  # 측정 중 표시
            sleep(6)
            
            wait_for_file(output_file_path)

            # Display prediction result from the file on LCD
            display_lcd_with_file(output_file_path)

            sleep(10)  # 대기 시간 
           
            lcd.lcd_clear()
            lcd.lcd_display_string("Device for GRED", 1)
            sleep(5)

            lcd.lcd_clear()
            sleep(1)  # 지워지고 나서 Delay

            lcd.lcd_display_string("Press the button", 1)
            sleep(5)

        else:
            # If the button is not pressed, turn off the LED
            GPIO.output(led_pin, GPIO.LOW)
           
except KeyboardInterrupt:
    GPIO.cleanup()