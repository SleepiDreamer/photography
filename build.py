import os
import sys
import cv2
import numpy as np

filelist = []
for file in os.listdir("original"):
    if file.endswith(".jpg"):
        filelist.append(file)

def compress_image(img, target_size, precision=3, min_quality=60):
    # Convert the image to JPEG format with quality 100
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    _, img_encoded = cv2.imencode(".jpg", img, encode_param)

    # Compress the image until its size is less than the target size
    while len(img_encoded) > target_size:
        # Reduce the JPEG quality by precision%
        encode_param[1] -= precision
        _, img_encoded = cv2.imencode(".jpg", img, encode_param)

        # If the quality drops below 60%, break out of the loop
        if encode_param[1] < min_quality:
            break

    # Decode the compressed image back to a cv2 image
    img_decoded = cv2.imdecode(np.frombuffer(img_encoded, np.uint8), cv2.IMREAD_COLOR)

    return img_decoded

def resize_image(img, longest_edge):
    # Get the dimensions of the image
    height, width = img.shape[:2]

    # If the image is already smaller than longest_edge on both sides, return the original image
    if height <= longest_edge and width <= longest_edge:
        return img

    # Calculate the scale factor to resize the image
    if height > width:
        scale = longest_edge / height
    else:
        scale = longest_edge / width

    # Resize the image using the scale factor
    resized_img = cv2.resize(img, (int(width * scale), int(height * scale)))

    return resized_img

n = 0
fastmode = input("Fast mode? (y/n): ")
fastmode = fastmode == "y"
for file in filelist:
    if not (fastmode and file in os.listdir("modal")):
        #using opencv to read the image, downsample it to 50% resolution
        img = cv2.imread("original/" + file)
        modal = resize_image(img, 1920)
        preview = resize_image(img, 1024)

        modal = compress_image(modal, 800000, 3, 60)
        preview = compress_image(preview, 150000, 3, 25)
        cv2.imwrite("modal/" + file, modal)
        cv2.imwrite("preview/" + file, preview)
        print(str(n) + "/" + str(len(filelist)) + " compressed " + file)
    n += 1


# n = 0
# for file in filelist:
#     #using opencv to read the image, downsample it to 50% resolution
#     img = cv2.imread("original/" + file)
#     if sys.getsizeof(img) < 3500000:
#         scale = 0.5
#     elif sys.getsizeof(img) < 7000000:
#         scale = 0.4
#     elif sys.getsizeof(img) < 9000000:
#         scale = 0.35
#     else:
#         scale = 0.6
    
#     #resize img to half resolution
#     width = int(img.shape[1] * scale)
#     height = int(img.shape[0] * scale)
#     dim = (width, height)
#     modal = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
#     if width < 1000:
#         scale = 0.7
#     else:
#         scale = 0.25
#     width = int(img.shape[1] * scale)
#     height = int(img.shape[0] * scale)
#     dim = (width, height)
#     preview = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#     #compress the image so it does not exceed 2000kb in size
#     if sys.getsizeof(img) > 10000000:
#         quality = 70
#     elif sys.getsizeof(img) > 7000000:
#         quality = 75
#     elif sys.getsizeof(img) > 5000000:
#         quality = 78
#     elif sys.getsizeof(img) > 3000000:
#         quality = 80
#     else:
#         quality = 92
#     cv2.imwrite("modal/" + file, modal, [cv2.IMWRITE_JPEG_QUALITY, quality])
#     cv2.imwrite("preview/" + file, preview, [cv2.IMWRITE_JPEG_QUALITY, 60])
#     n += 1
#     print(str(n) + "/" + str(len(filelist)) + " compressed " + file)