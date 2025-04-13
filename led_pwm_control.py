import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep

# GPIO Setup
GPIO.setmode(GPIO.BCM)
LED_PINS = {'red': 17, 'green': 27, 'blue': 22}

# Initialize PWM for each LED
pwm_leds = {}
for color, pin in LED_PINS.items():
    GPIO.setup(pin, GPIO.OUT)
    pwm_leds[color] = GPIO.PWM(pin, 1000)  # 1000Hz frequency
    pwm_leds[color].start(0)  # Start with 0% duty cycle

def update_intensity(color, value):
    """Update LED intensity based on slider value (0-100)"""
    pwm_leds[color].ChangeDutyCycle(float(value))

def cleanup():
    """Clean up GPIO on exit"""
    for pwm in pwm_leds.values():
        pwm.stop()
    GPIO.cleanup()
    root.destroy()

# Create GUI
root = tk.Tk()
root.title("LED Intensity Controller")

# Sliders for each LED
for color in LED_PINS:
    tk.Label(root, text=f"{color.capitalize()} LED").pack()
    slider = tk.Scale(root, from_=0, to=100, orient='horizontal',
                      command=lambda val, c=color: update_intensity(c, val))
    slider.pack()

# Exit button
tk.Button(root, text="Exit", command=cleanup).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", cleanup)
root.mainloop()