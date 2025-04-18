import cv2
import numpy as np
import pytesseract
import re
from passporteye import read_mrz

def extract_passport_data(image_bytes: bytes):
    # Convert bytes to image file
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Configure Tesseract OCR settings
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    custom_config = r'--oem 0 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<'  
    
    # Save temporary file because passporteye works with file paths
    temp_file = "/tmp/passport.jpg"
    cv2.imwrite(temp_file, img)

    mrz = read_mrz(temp_file, extra_cmdline_params=custom_config)
    if mrz:
        mrz_dict = mrz.to_dict()
        # Clean and format name fields
        for key in ['names', 'surname']:
            if key in mrz_dict and mrz_dict[key]:
                # Remove multiple spaces and replace K sequences (more than 3)
                value = re.sub(r'\s+', ' ', mrz_dict[key].strip())
                value = re.sub(r'K{4,}', lambda m: '<' * len(m.group()), value)
                mrz_dict[key] = value
        return mrz_dict
    else:
        return {"error": "Could not extract MRZ"}
