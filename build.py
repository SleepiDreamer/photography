import os
import sys
import cv2

filelist = []
for file in os.listdir("original"):
    if file.endswith(".jpg"):
        filelist.append(file)

n = 0
for file in filelist:
    #using opencv to read the image, downsample it to 50% resolution
    img = cv2.imread("original/" + file)
    if sys.getsizeof(img) < 3500000:
        scale = 0.5
    elif sys.getsizeof(img) < 7000000:
        scale = 0.4
    elif sys.getsizeof(img) < 9000000:
        scale = 0.35
    else:
        scale = 0.6
    
    #resize img to half resolution
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    modal = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    width = int(img.shape[1] * 0.25)
    height = int(img.shape[0] * 0.25)
    dim = (width, height)
    preview = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
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
    cv2.imwrite("modal/" + file, modal, [cv2.IMWRITE_JPEG_QUALITY, quality])
    cv2.imwrite("preview/" + file, preview, [cv2.IMWRITE_JPEG_QUALITY, 60])
    n += 1
    print(str(n) + "/" + str(len(filelist)) + " compressed " + file)
    