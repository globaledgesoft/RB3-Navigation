#on windows install pygame and numpy - 'py -m pip install numpy','py -m pip install pygame' 
#linux - 'pip install numpy','pip install pygame'. DIDN'T RUN THE PROGRAM ON LINUX 
#move mouse button inside pygame window to begin the SHOW - with auto-rewind!!!
#prepared by GlobalEdge Software, Bangalore
#author : ss.pandiri@globaledgesoft.com
import pygame
import numpy as np
import os

#configure cam near and far here. program draws red pixels in case 
#there's no data in the depth image between cam near and far
#for float/other data change dtype appropriately
cam_ranges = np.array([500, 4500], dtype=np.uint16)

#configure near and far for the test. program draws a green pixel if distance
#data is found within the ranges below
#for float/other data change dtype appropriately
my_ranges = np.array([500, 1000], dtype=np.uint16)

#read current directory that stores depth images and sort filenames date wise
#save the depth_image_viewer.py in a folder other than where depth-image are stored
arr = os.listdir('.')
arr.sort(key=os.path.getctime)
f_cnt = len(arr)
print(f_cnt)

#configure your image width and height here
I_HEIGHT = 480
I_WIDTH = 640

pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((800,600))
gameDisplay.fill(black)
pixAr = pygame.PixelArray(gameDisplay)

print(my_ranges)
#print('done processing')

n = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEMOTION:
            gameDisplay.fill(black)
            idataraw = np.fromfile(arr[n], dtype=np.uint16)
            print(arr[n])
            n = n+1
            if (n >= f_cnt):
                n = 0;
            idata = idataraw.reshape(I_HEIGHT , I_WIDTH)

            print(idata[239])
            print(idata[240])

            for i in range(0, 480):
                for j in range(I_WIDTH):
                    val = idata[i, j]
                    if val < cam_ranges[0]:
                        pixAr[j][i] = red
                    elif val > cam_ranges[1]:
                        pixAr[j][i] = blue
                    elif val <= my_ranges[1]:
                        if val >= my_ranges[0]:
                            pixAr[j][i] = green

    pygame.display.update()
