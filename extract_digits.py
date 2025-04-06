# ocr_work code with comments

import pytesseract
import cv2
import numpy as np
import re

# Load the image
img = cv2.imread(r"C:\Users\Khushi\Desktop\ocr\images\ocr_2.jpg")

# Check if the image loaded correctly
if img is None:
    print("Error: Image not found!")
    exit()

# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to smooth the image and reduce noise
blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

# Adaptive thresholding to handle varying lighting conditions across the image
bwimg = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)

# Invert the image for better OCR results (black text on white background)
imgbit = cv2.bitwise_not(bwimg)

# Dilation followed by erosion to connect text parts
kernel = np.ones((3, 3), np.uint8)
img_dilate = cv2.dilate(imgbit, kernel, iterations=2)
img_erode = cv2.erode(img_dilate, kernel, iterations=1)

# Optional: Inversion to match Tesseract's expected input (black text on white background)
img_processed = cv2.bitwise_not(imgbit)

# Show the processed image for debugging purposes
cv2.imshow("Processed Image", img_processed)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Run Tesseract OCR on the processed image
ocr_res = pytesseract.image_to_string(img_processed, config='outputbase digits')

# Debugging: Print the raw OCR output
print("Raw OCR Output:")
print(ocr_res)

# Use regex to capture numbers that may include decimals, such as '12.3', '45.67'
# Adjust the regex to match numbers (including decimals, if present)
regex = r"\d+(\.\d+)?"  # Matches integers or decimals like 12.3 or 45

# Find all numbers in the OCR result
numbers = re.findall(regex, ocr_res)

# Print the detected numbers
if numbers:
    print("Detected Numbers:", numbers)
else:
    print("No matching numbers found.")
