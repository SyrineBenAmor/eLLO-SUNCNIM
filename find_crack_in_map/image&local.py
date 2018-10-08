# save treated image with same name of the original imag
# open picture file
# read pictures name
#stock picture name
#comparaison name picture with la colonne du temps dans le fichier data.*txt
# afficher la ligne qui correspond au meme temps
import glob
import cv2
import time
pathImage = "gather_Data/photos/test.08-10-2018/*.jpg"
nameDatafile = "gather_Data/data/08-10-2018Data.txt"
i =0

def transformTimeToSec (time): #(%H:%M:%S)
    h,m,s = time.split(":")
    time_in_sec = int(h) * 3600 + int(m) * 60 +int(s)
    return (time_in_sec)
def time_data_transform(n):
    divide_Time = time.localtime(n)
    hour  = time.localtime(n)[3]
    minute = time.localtime(n)[4]
    sec = time.localtime(n)[5]
    return hour,minute,sec

def comparaisonBetweenImageTimeAndDataTime(nameDatafile,pathImage):
    for imagePath in glob.glob(path):
        i+=1
    
        image_time = imagePath.split('.')[-2]
        image_time_hour = image_time.split(':')[0]
        image_time_minute = image_time.split(':')[1]
        image_time_sec = image_time.split(':')[2]
    
 
    fichier = open(nameDatafile,'r') 

    for ligne in fichier:
        time_data=ligne.split(":")[0]
        hour,minute,sec =time_data_transform(time_data)
        if(hour=image_time_hour and minute=image_time_minute and sec=image_time_sec):
            print(ligne)
        
    fichier.close()