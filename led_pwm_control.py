import tkinter as tk
import RPi.GPIO as GPIO

# GPIO Setup (Using YOUR pin numbers)
GPIO.setmode(GPIO.BCM)
LED_PINS = {
    'red': 8,    # Physical Pin 24
    'green': 7,  # Physical Pin 26
    'blue': 1    # Physical Pin 28
}

# Initialize PWM
pwm_leds = {}
for color, pin in LED_PINS.items():
    GPIO.setup(pin, GPIO.OUT)
    pwm_leds[color] = GPIO.PWM(pin, 1000)  # 1000Hz frequency
    pwm_leds[color].start(0)  # Start at 0% brightness

def update_intensity(color, value):
    """Update LED brightness (0-100%)"""
    brightness = float(value)
    pwm_leds[color].ChangeDutyCycle(brightness)
    print(f"{color} LED (GPIO {LED_PINS[color]}) set to {brightness}%")

def cleanup():
    """Turn off all LEDs safely"""
    for color in pwm_leds:
        pwm_leds[color].stop()
    GPIO.cleanup()
    root.destroy()

# Create GUI
root = tk.Tk()
root.title("LED Controller (Your Pins)")

# Sliders for each LED
for color in LED_PINS:
    frame = tk.Frame(root)
    frame.pack(pady=5)
    
    tk.Label(frame, text=f"{color.upper()} (GPIO {LED_PINS[color]}):").pack(side='left')
    tk.Scale(
        frame,
        from_=0,
        to=100,
        orient='horizontal',
        command=lambda val, c=color: update_intensity(c, val)
    ).pack(side='left')

# Exit button
tk.Button(root, text="EXIT", command=cleanup).pack(pady=20)

# Handle window close
root.protocol("WM_DELETE_WINDOW", cleanup)
root.mainloop()
