import cv2
import numpy as np
import pytesseract
from passporteye import read_mrz

def extract_passport_data(image_bytes: bytes):
    # Convert bytes to image file
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Save temporary file because passporteye works with file paths
    temp_file = "/tmp/passport.jpg"
    cv2.imwrite(temp_file, img)

    mrz = read_mrz(temp_file)
    if mrz:
        return mrz.to_dict()
    else:
        return {"error": "Could not extract MRZ"}
