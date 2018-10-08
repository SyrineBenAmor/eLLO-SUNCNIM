# save treated image with same name of the original imag
# open picture file
# read pictures name
#stock picture name
#comparaison name picture with la colonne du temps dans le fichier data.*txt
# afficher la ligne qui correspond au meme temps
import glob
import cv2
import time
path = "Image_processing/image_processing_output/folderFissure/*.jpg"
nameDatafile = "17-09-2018Data.txt"
#**************** transform name's image to time in sec*******************

for imagePath in glob.glob(path):
    i+=1
    print(imagePath)
    imagePath = imagePath.split('.')
    temps  = imagePath.remove(".jpg")
    print(temps)
    
#******************Open data file to compare time with name image****************
ma_liste=[]
fichier = open(nameDatafile)
 
for ligne in fichier:
    a=ligne.replace(",","")
    b=a.split()
    for i in range(len(b)):
        c=b[i]
        d=ma_liste.append(c)
print(d)

 
fichier.close()
#****************afficher les données correspondantes*********************

k = cv2.waitKey(0)
if k == 27: #wait for ESC key to exit
    cv2.destroyAllWindows()
print ('end')
