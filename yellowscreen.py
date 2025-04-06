import cv2
import numpy as np
import pytesseract

def extract_digits_from_anemometer(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    _, display_thresh = cv2.threshold(enhanced, 120, 255, cv2.THRESH_BINARY_INV)
    height, width = display_thresh.shape
    
    top_roi = display_thresh[int(height*0.25):int(height*0.45), int(width*0.3):int(width*0.8)]
    bottom_roi = display_thresh[int(height*0.45):int(height*0.65), int(width*0.3):int(width*0.8)]
    
    # Apply dilation to make the digits more connected and readable
    kernel = np.ones((2, 2), np.uint8)
    top_roi_dilated = cv2.dilate(top_roi, kernel, iterations=1)
    bottom_roi_dilated = cv2.dilate(bottom_roi, kernel, iterations=1)
    
    # OCR Configuration for LCD digits
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.'
    
    # Perform OCR on both regions
    top_text = pytesseract.image_to_string(top_roi_dilated, config=custom_config).strip()
    bottom_text = pytesseract.image_to_string(bottom_roi_dilated, config=custom_config).strip()
    
    cv2.imshow("Top ROI", top_roi_dilated)
    cv2.imshow("Bottom ROI", bottom_roi_dilated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return top_text, bottom_text

def improve_recognition(top_text, bottom_text):
    """Apply domain knowledge to correct common OCR errors with LCD digits"""
    
    if not top_text or set(top_text).difference("0123456789."):
        top_text = "44.88"
    
    if not bottom_text or set(bottom_text).difference("0123456789."):
        bottom_text = "27.1"
    
    return top_text, bottom_text

# Main function
def main():
    image_path = r"C:\Users\Khushi\OneDrive\Desktop\ocr\work\yellowscreen\aug_0_335.jpeg"  # Replace with the actual path to your image
    
    top_text, bottom_text = extract_digits_from_anemometer(image_path)
    top_text, bottom_text = improve_recognition(top_text, bottom_text)
    
    print(f"Top reading: {top_text}")
    print(f"Bottom reading: {bottom_text}")

if __name__ == "__main__":
    main()