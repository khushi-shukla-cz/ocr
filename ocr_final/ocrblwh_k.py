import pytesseract
import cv2
import numpy as np
import re
import os
import matplotlib.pyplot as plt

def show_image(title, image):
    plt.figure(figsize=(6, 6))
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def whitescreen(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    _, bwimg = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    imgbit = cv2.bitwise_not(bwimg)
    kernel = np.ones((2, 2), np.uint8)
    imgdilate = cv2.dilate(imgbit, kernel, iterations=2)
    imgdilate = cv2.bitwise_not(imgdilate)

    show_image("White Screen Processed Image", imgdilate)

    ocrres = pytesseract.image_to_string(imgdilate)

    regex1 = r'(\d) (\d)'
    regex2 = r'(\d)(\d)'
    regex3 = r'(\d) (\d)\.(\d)'
    regex4 = r'(\d)(\d)\.(\d)(\d)'

    match1 = re.search(regex1, ocrres)
    match2 = re.search(regex2, ocrres)
    match3 = re.search(regex3, ocrres)
    match4 = re.search(regex4, ocrres)

    if match1:
        print(match1.group(1), end="")
        print(match1.group(2))
    elif match2:
        print(match2.group(1), end="")
        print(match2.group(2))
    elif match3:
        print(match3.group(1), end="")
        print(match3.group(2), end="")
        print(match3.group(3))
    elif match4:
        print(match4.group())

def bluescreen(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    _, bwimg = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    imgbit = cv2.bitwise_not(bwimg)
    kernel = np.ones((2, 2), np.uint8)
    imgdilate = cv2.erode(imgbit, kernel, iterations=3)
    imgdilate = cv2.bitwise_not(imgdilate)

    show_image("Blue Screen Processed Image", imgdilate)

    ocrres = pytesseract.image_to_string(imgdilate)

    if not ocrres.strip():
        kernel = np.ones((2, 1), np.uint8)
        imgdilate = cv2.erode(imgbit, kernel, iterations=3)
        imgdilate = cv2.bitwise_not(imgdilate)
        ocrres = pytesseract.image_to_string(imgdilate)

    regex1 = r'^\d\d\.\d'
    regex2 = r'^\d\d'
    regex3 = r'^\d\.\d'
    regex4 = r'^\d\d\.\d\d\d'
    regex5 = r'^. \d\d\d\d'

    for pattern in [regex1, regex2, regex3, regex4, regex5]:
        match = re.search(pattern, ocrres)
        if match:
            print(match.group())
            break

def preprocess(img):
    if len(img.shape) < 3 or img.shape[2] < 3:
        print("Invalid image format.")
        return

    pixel = img[30, 10]  # BGR pixel at (30,10)
    b, g, r = pixel

    if b > g and b > r and b < 200:
        bluescreen(img)
    else:
        whitescreen(img)

# Main execution
files = [r"ocr3.png"]

for filename in files:
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue

    img = cv2.imread(filename)
    if img is None:
        print(f"Unable to read image: {filename}")
        continue

    preprocess(img)
