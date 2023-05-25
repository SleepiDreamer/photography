import os
import sys
import cv2

filelist = []
for file in os.listdir("fullres"):
    if file.endswith(".jpg"):
        filelist.append(file)

n = 0
for file in filelist:
    #using opencv to read the image, downsample it to 50% resolution
    img = cv2.imread("fullres/" + file)
    if sys.getsizeof(img) < 3500000:
        halfres = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    elif sys.getsizeof(img) < 7000000:
        halfres = cv2.resize(img, (0,0), fx=0.4, fy=0.4)
    elif sys.getsizeof(img) < 9000000:
        halfres = cv2.resize(img, (0,0), fx=0.35, fy=0.35)
    else:
        halfres = img
    #compress the image so it does not exceed 2000kb in size
    if sys.getsizeof(img) > 10000000:
        quality = 70
    elif sys.getsizeof(img) > 7000000:
        quality = 75
    elif sys.getsizeof(img) > 5000000:
        quality = 78
    elif sys.getsizeof(img) > 3000000:
        quality = 80
    else:
        quality = 92
    cv2.imwrite("halfres/" + file, halfres, [cv2.IMWRITE_JPEG_QUALITY, quality])
    n += 1
    print(str(n) + "/" + str(len(filelist)) + " compressed " + file)
    