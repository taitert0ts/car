from microbit import *
import radio
import neopixel

# --- Pin Assignments ---
LEFT_MOTOR = pin0
RIGHT_MOTOR = pin1
LEFT_LINE_SENSOR = pin2
RIGHT_LINE_SENSOR = pin3
ULTRASONIC_TRIG_PIN = pin8
ULTRASONIC_ECHO_PIN = pin12
HEADLIGHTS_PIN = pin13
BUZZER_PIN = pin16

# --- Neopixel Setup (For RGB LED) ---
lights = neopixel.NeoPixel(HEADLIGHTS_PIN, 1)

# --- Global Variables ---
line_following_mode = False
obstacle_avoidance_mode = False
current_speed = 50
white_threshold = 500
black_threshold = 200
headlights_on = False
bluetooth_control_mode = False

# --- Motor Control Functions ---

def forward():
    LEFT_MOTOR.write_digital(current_speed)
    RIGHT_MOTOR.write_digital(current_speed)

def backward():
    LEFT_MOTOR.write_digital(-current_speed)
    RIGHT_MOTOR.write_digital(-current_speed)

def turn_left():
    LEFT_MOTOR.write_digital(0)
    RIGHT_MOTOR.write_digital(current_speed)

def turn_right():
    LEFT_MOTOR.write_digital(current_speed)
    RIGHT_MOTOR.write_digital(0)

def stop():
    LEFT_MOTOR.write_digital(0)
    RIGHT_MOTOR.write_digital(0)

def faster():
    global current_speed
    current_speed = min(current_speed + 10, 100)

def slower():
    global current_speed
    current_speed = max(current_speed - 10, 0)

# --- Line Following Function ---

def follow_line():
    left_value = LEFT_LINE_SENSOR.read_digital()
    right_value = RIGHT_LINE_SENSOR.read_digital()

    if left_value == 0 and right_value == 1:
        turn_left(40)  # Assuming you want to turn at a slower speed
    elif left_value == 1 and right_value == 0:
        turn_right(40) # Assuming you want to turn at a slower speed
    else:
        forward()

# --- Obstacle Avoidance Function (Placeholder) ---

def avoid_obstacles():
    # Add your ultrasonic sensor code here
    pass

# --- Other Functions ---

def toggle_headlights():
    global headlights_on
    headlights_on = not headlights_on
    lights[0] = (255, 255, 255) if headlights_on else (0, 0, 0)
    lights.show()

def honk():
    buzzer.write_digital(1)
    sleep(100)
    buzzer.write_digital(0)

def random_light_show():
    # Add your custom light show code here
    pass

# --- Radio Setup ---
radio.on()
radio.config(channel=7)
radio.config(power=7)

# --- Main Loop ---

while True:
    # --- Toggle Control Mode (Keyboard vs. Bluetooth) ---
    if button_a.is_pressed() and button_b.is_pressed():
        if bluetooth_control_mode:
            display.scroll("Keyboard Mode")
        else:
            display.scroll("Bluetooth Mode")
        bluetooth_control_mode = not bluetooth_control_mode
        sleep(500)

    if bluetooth_control_mode:
        # --- Bluetooth Control Mode ---
        incoming = radio.receive()
        if incoming:
            # Process Bluetooth commands here (e.g., 'F' for forward, 'B' for backward, etc.)
            if incoming == 'F':
                forward()
            elif incoming == 'B':
                backward()
            # ... (Add more commands for steering, lights, etc.)
    else:
        # --- Keyboard Control Mode ---
        if button_a.is_pressed():
            break
        incoming = uart.read()
        if incoming:
            key = incoming.decode("utf-8")
            if key == 'w':
                forward()
            elif key == 's':
                backward()
            elif key == 'a':
                turn_left()
            elif key == 'd':
                turn_right()
            elif key == ' ':
                stop()
            elif key == 'l':
                toggle_headlights()
            elif key == 'h':
                honk()
            elif key == 'f':
                faster()
            elif key == 'o':
                slower()
            else:
                display.scroll("Invalid Key")
            sleep(100)

    # --- Automatic Modes ---
    if line_following_mode:
        follow_line()
    if obstacle_avoidance_mode:
        avoid_obstacles()

    sleep(100)
