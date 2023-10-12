import time

#origin source
# https://upload.wikimedia.org/wikipedia/commons/7/74/%22I_Got_an_Idea%5E_If_it%27s_Good...I%27ll_Cash_In%22_-_NARA_-_514560_-_retouched.jpg
# https://commons.wikimedia.org/wiki/Category:Large_images 

import cv2


start_time = time.perf_counter()
img = cv2.imread('origin.jpg')
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"CV2 READ: Execution time: {execution_time:.4f} seconds")


start_time = time.perf_counter()
cv2.imwrite('cv2_origin.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 85])
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"CV2 COMPRESS: Execution time: {execution_time:.4f} seconds")

from PIL import Image
start_time = time.perf_counter()
image = Image.open("origin.jpg")
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"PIL READ: Execution time: {execution_time:.4f} seconds")

# Compress and save the image
start_time = time.perf_counter()
image.save("pil_origin.jpg", optimize=True, quality=85)
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"PIL COMPRESS: Execution time: {execution_time:.4f} seconds")