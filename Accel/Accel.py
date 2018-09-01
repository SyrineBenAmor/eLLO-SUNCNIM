'''Prints the accelerometer values every second.'''
import time
import datetime
from microstacknode.hardware.accelerometer.mma8452q import MMA8452Q
import math


G_RANGE = 2
INTERVAL = 0.5  # seconds
adjustZ = 9.80665 #standard Gravity
distance_intial = 0


def getAcceleration():
    with MMA8452Q() as accelerometer:
        # Configure accelerometer
        accelerometer.standby()
        accelerometer.set_g_range(G_RANGE)
        accelerometer.activate()
        print("g = {}".format(G_RANGE))
        time.sleep(INTERVAL)  # settle
        
        
        while True:
            #declare time
            initial_time = time.time()
            delta= datetime.timedelta(seconds = 1)  # delta =    0:00:01
            next_time = datetime.datetime.now()     #next_time =  12:00:36.212448 
            dt = datetime.datetime.now()            # dt =        12:00:36.229735

            #******************* get data from sensor ,,open text file and store it *************************************
            
            if dt>next_time:
                file = open("Accelertion.txt","a+") # a+ : open for reading and write at the end of file
                raw = accelerometer.get_xyz(raw=True)
                g = accelerometer.get_xyz()
                ms = accelerometer.get_xyz_ms2()
                print("----")
                print(datetime.datetime.now())
                print('  raw | x: {}, y: {}, z: {}'.format(raw['x'],raw['y'],raw['z']))
                print('    G | x: {:.2f}, y: {:.2f}, z: {:.2f}'.format(g['x'],g['y'],g['z']))
                X = ms['x']
                Y = ms['y']
                Z = ms['z'] - adjustZ
                print('m/s^2 | x: {:.2f}, y: {:.2f}, z: {:.2f}'.format(X,Y,Z))
                
                total_axes = math.sqrt(X**2+Y**2+Z**2)
                print("total_axes: "+str(total_axes)+"m/s^2")
                
                # calcul angles and conversion in degree
                angleX = round(math.asin(X/ total_axes )*180.0/3.1416)
                angleY = round(math.asin(Y/ total_axes )*180.0/3.1416)
                angleZ = round(math.acos(Z/ total_axes )*180.0/3.1416)
                #print('anglex', angleX)
                #print('angley', angleY)
                #print('anglez', angleZ)

                #save data 
                file.write("{},{}\n".format(time.time(),total_axes))
                file.close()
                next_time= dt + delta
                time.sleep(INTERVAL)
    return(total_axes)    
#**************************create new text file to store distance*****************************************

def calculateDistance (total_axes):               
    t= time.time()-initial_time
    #print("time = " + str(t))
    file = open("Distance.txt","a+")
    #calculate distance every tow consecutive times
    distance_now = (0.5* total_axes* (t)**2)*100
    print("distance=  "+str(Distance)+"cm")
    #calculate total distance at the end of process
    distance_total = distance_intial+ distance_now 
    distance_intial = distance_total
    print("distance total = " + str(distance_total)+"cm")
    #save modified file
    file.write("{},{}\n".format(time.time(),distance_now))
    file.close()
    time.sleep(INTERVAL)
    return(distance_total )
                
               
            
                
