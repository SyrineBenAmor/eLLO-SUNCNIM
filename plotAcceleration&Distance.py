import matplotlib.pyplot as plt
import numpy as np
import csv
import cv2

pathToDistanceFile = 'Distance.txt'
pathToAngleFile = 'Angle.txt'

t=[]
anglex=[]
angley=[]
anglez=[]


def plotDistance():
    #********************** Distance Graphe*****************
    time = [];DistanceX=[];DistanceY=[];DistanceZ=[]
    with open(pathToDistanceFile,'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            time.append(row[0])
            DistanceX.append(row[1])
            DistanceY.append(row[2])
            DistanceZ.append(row[3])
    plt.figure(2)      
    plt.plot(DistanceX,label = 'DistanceX', color= 'red')
    #plt.plot(DistanceX,label = 'DistanceY', color= 'blue')
    #plt.plot(DistanceX,label = 'DistanceZ', color= 'green')
    plt.xlabel('t(s)')
    plt.ylabel('Ditance(mm)')
    plt.title('graph distance')
    plt.legend()
    plt.show()
#********************** Acceleration Graphe*****************
with open(pathToAngleFile,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        t.append(row[0])
        anglex.append(row[1])
        angley.append(row[2])
        anglez.append(row[3])
        
plt.figure(1) 
plt.plot(anglex,label = 'angle axe X ', color= 'red')
#plt.plot(angley,label = 'angle axe Y', color= 'blue')
#plt.plot(anglez,label = 'angle axe Z', color= 'green')

plt.xlabel('t')
plt.ylabel('x,y,z')
plt.title('graph angle')
plt.legend()
#plt.savefig('graph3.png')
plotDistance()


