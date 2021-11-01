import numpy as np
import cv2 as cv
import math
from matplotlib import pyplot as plt

position=[]
i=0
print('Odaberite dvije rubne točke')
# funkcija u kojoj su ispisane naredbe za detekciju dvostrukog klika miša, crtanje točke,
# ispisivanje koordinata točaka, crtanje linije između točaka te crtanje i izračunavanje centra
# nadalje svakim sljedećim klikom izračunava se udaljenost od centra do točke u mm
def draw_circle(event,x,y,flags,param):
    global position,i 
    #detekcija dvostrukog klika miša, crtanje točke i spremanje i ispisivanje koordinata
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(resized_image,(x,y),2,(255,0,0),-1) # crtanje točke
        #spremanje koordinata
        position.append(x)  
        position.append(y)
        # ispisivanje koordinata
        print('x = %d, y = %d'%(x, y)) 
        # svakim dvostrukim klikom miša vrijednost se povećava (služi za brojanje točaka)
        i=i+1 
        if i==2: # ukoliko su odabrane prve dvije rubne točke:
            # crtanje linije između točaka
            cv.line(resized_image,(position[0],position[1]),(position[2],position[3]),(255,255,255),1) 
            # računanje centra između prve dvije točke
            cenX=(position[0]+position[2])/2 
            cenY=(position[1]+position[3])/2
            cv.circle(resized_image,(int(cenX),int(cenY)),2,(255,0,0),-1) # crtanje točke u centru
            print('centar: x= %d, y = %d'%(cenX,cenY)) # ispisivanje centra
            # računanje udaljenosti
            distance=math.sqrt(abs(position[2]-position[0])**2 + abs(position[3]-position[1])**2) 
            # broj 0.02906976744 dobiven je djeljenjem stvarne udaljenosti sa pixelima na fotografiji
            distanceMM=0.02906976744*distance 
            # ispis stvarne udaljenosti u mm
            print('Udaljenost između točaka iznosi:'+str(distanceMM*10)+'mm') 
            print('Odaberite sljedeću točku za mjerenje udaljenosti')
        if i>2: # za svaku sljedeću točku 
            cenX=(position[0]+position[2])/2
            cenY=(position[1]+position[3])/2
            # crtanje linije između centra i sljedeće točke
            cv.line(resized_image,(int(cenX),int(cenY)),(position[i+1],position[i+2]),(255,255,255),1) 
            distance=math.sqrt(abs(cenX-position[i+1])**2 + abs(cenY-position[i+2])**2)
            distanceMM=0.02906976744*distance
            print('Udaljenost od centra do točke:'+str(distanceMM*10)+ 'mm')
            i=i+1
            print('Odaberite sljedeću točku za mjerenje udaljenosti')

# funkcija za skaliranje slike        
def rescaleFrame (frame,scale=0.2):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img=cv.imread('Photos/sat2.jpg') # učitavanje fotografije
resized_image=rescaleFrame(img)
#canny=cv.Canny(resized_image,100,200) # crtanje konture 
cv.imshow('image',resized_image)
cv.setMouseCallback('image',draw_circle) # pozivanje funkcije 
while(1):
    cv.imshow('image',resized_image)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()

    

