"""
This code checks the temperature of the raspberry pi's CPU
and displays the value on the LEDs of the SensHat.
Additionally, it changes the colour of the LEDs based on
the temperature value being displayed.
"""
try:
    from time import sleep
    from sense_hat import SenseHat
except:
    print("Could not import the required modules")

sense = SenseHat()
sense.low_light = True
def checkTemp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    temp = round(temp)
    #print (temp, " degrees celcius")
    return temp

def main():
    white = (255, 255, 255)
    red = (100, 0, 0)
    none = (0, 0, 0)
    colour = white
    while True:
        temp = int(checkTemp())
        if temp >= 50:
            colour = red
        else:
            colour = white
        temp = str(temp)
        sense.show_message(temp, text_colour=colour, back_colour=none)
        sleep(5)
        
if __name__ == '__main__':
    main()