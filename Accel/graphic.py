
import matplotlib.pyplot as plt
import numpy as np
import csv
import cv2
t= []
total=[]
Distance=[]
y=[]
z=[]
#********************** Acceleration Graphe*****************
with open('Accelertion.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        t.append(row[0])
        total.append(row[1])
        #y.append(row[2])
        #z.append(row[3])
        
plt.figure(1) 
plt.plot(total,label = 'acceleration sur 3 axes', color= 'green')
#plt.plot(y,label = 'acceleration axe Y', color= 'yellow')
#plt.plot(z,label = 'acceleration axe Z', color= 'red')

plt.xlabel('t')
plt.ylabel('x,y,z')
plt.title('graph acceleration')
plt.legend()
#plt.savefig('graph3.png')

#********************** Distance Graphe*****************
with open('Distance.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        t.append(row[0])
        Distance.append(row[1])
plt.figure(2)      
plt.plot(Distance,label = 'Distance', color= 'red')
plt.xlabel('t(s)')
plt.ylabel('Ditance(cm)')
plt.title('graph distance')
plt.legend()
plt.show()
