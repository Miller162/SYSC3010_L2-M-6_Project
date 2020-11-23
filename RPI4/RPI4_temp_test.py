from time import sleep
#Check temp of RPI CPU
def checkTemp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    print (temp)

if __name__ == "__main__":
    while True:
        checkTemp()
        sleep(5)