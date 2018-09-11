'''Prints the latitude and longitude every second.'''
import time
import microstacknode.hardware.gps.l80gps 

gps = microstacknode.hardware.gps.l80gps.L80GPS()

def getGPSvalue():
    data = gps.get_gprmc()
    lat = data.get("latitude")
    long = data.get("longitude")
    print(lat,long)
    file = open("GPSvalue.txt","a+")
    file.write("{},{},{}\n".format(time.time(),lat,long))
    #time.sleep(1)
        
    file.close()
    return (lat,long)
