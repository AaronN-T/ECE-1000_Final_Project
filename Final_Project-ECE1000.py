from PicoBreadboard import LED, BUZZER, BUTTON
from utime import sleep
from random import choice
import ssd1306

# I2C setup for OLED display
i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# RGB LEDs
Red_LED = LED(2)
Green_LED = LED(3)
Blue_LED = LED(4)

# Buttons
BUT1 = BUTTON(6)  # Red Button
BUT2 = BUTTON(7)  # Green Button
BUT3 = BUTTON(8)  # Blue Button
BUT4 = BUTTON(9)  # Exit Button

# Buzzer
Buzz = BUZZER(15)

# Predefined colors for patterns
colors = ["Red", "Green", "Blue"]

# Function to light up LEDs
def Light_Up(color, duration=0.5):
    Red_LED.off()
    Green_LED.off()
    Blue_LED.off()
    
    if color == "Red":
        Red_LED.on()
    elif color == "Green":
        Green_LED.on()
    elif color == "Blue":
        Blue_LED.on()
        
    sleep(duration)
    
    Red_LED.off()
    Green_LED.off()
    Blue_LED.off()

# Function to read button input
def Button_Pressed():
    while True:
        if BUT4.read():  # Exit button
            return "Exit"
        if BUT1.read():
            return "Red"
        elif BUT2.read():
            return "Green"
        elif BUT3.read():
            return "Blue"
        sleep(0.1)

# Function to display a message on OLED
def Display(lines, duration=1):
    oled.fill(0)
    for idx, line in enumerate(lines):
        oled.text(line, 0, idx * 8)
    oled.show()
    sleep(duration)
    oled.fill(0)
    oled.show()

# Function to select difficulty
def Select_Difficulty():
    Display(["Select Difficulty:", "1: Easy", "2: Medium", "3: Hard"], duration=3)
    
    while True:
        if BUT1.read():  # Easy
            return "Easy", 1.0, 0.5
        elif BUT2.read():  # Medium
            return "Medium", 0.5, 0.3
        elif BUT3.read():  # Hard
            return "Hard", 0.2, 0.1

# Main Simon Says game logic
def Simon_Says():
    while True:
        # Choose difficulty
        difficulty, display_time, input_time = Select_Difficulty()
        Display([f"Mode: {difficulty}"], duration=2)
        
        while True:
            # Generate a new sequence of exactly 3 colors
            Rand_Seq = [choice(colors) for _ in range(3)]
            
            print("Watch the pattern!")
            Display(["Watch the", "pattern!"], duration=1)
            
            # Show the sequence
            for color in Rand_Seq:
                Light_Up(color, display_time)
                sleep(0.3)
            
            print("Your turn!")
            Display(["Your turn!"], duration=1)
            
            # Player's turn
            for color in Rand_Seq:
                player_input = Button_Pressed()
                
                if player_input == "Exit":  # Handle exit
                    Display(["Exiting Game..."], duration=2)
                    return
                
                if player_input != color:
                    print("Game Over!")
                    Display(["Game Over!", "You lost."], duration=2)
                    
                    # Buzzer feedback
                for _ in range(2):
                    Buzz.on()
                    sleep(0.5)
                    Buzz.off()
                    sleep(0.2)
                return  # End the game
            
                # Positive feedback
                print("Correct!")
                Display(["Correct!"], duration=0.5)
                for _ in range(2):
                    Buzz.on()
                    sleep(0.1)
                    Buzz.off()
                    sleep(0.1)

            # Clear the sequence and prepare for the next round
            print("Next round!")
            Display(["Next round!"], duration=1)
            sleep(input_time)

# Run the game
Simon_Says()
    
        
        
        
        