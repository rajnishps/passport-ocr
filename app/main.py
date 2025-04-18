from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from passporteye import read_mrz
from io import BytesIO
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post("/extract")
async def extract_mrz(file: UploadFile = File(...)):
    # Read the uploaded file as bytes
    image_data = await file.read()
    
    # Convert bytes into a file-like object
    image = BytesIO(image_data)
    
    # Extract MRZ data using PassportEye
    mrz = read_mrz(image)
    
    if mrz:
        # Extracted MRZ data as a dictionary
        mrz_dict = mrz.to_dict()
        
        # Reformat the dates to 'DD-MM-YYYY'
        def reformat_date(date_str: str):
            try:
                # Convert YYMMDD to DD-MM-YYYY
                return datetime.strptime(date_str, "%y%m%d").strftime("%d-%m-%Y")
            except ValueError:
                return None  # Return None if the date is invalid
        
        # Reformat date_of_birth and expiration_date
        mrz_dict["date_of_birth"] = reformat_date(mrz_dict.get("date_of_birth", ""))
        mrz_dict["expiration_date"] = reformat_date(mrz_dict.get("expiration_date", ""))
        
        # Keep the << as placeholders and clean up other fields accordingly
        mrz_dict["names"] = mrz_dict.get("names", "").strip()
        mrz_dict["surname"] = mrz_dict.get("surname", "").strip()

        # Return the formatted MRZ data
        return {"mrz_data": mrz_dict}
    else:
        # Return an error message if MRZ is not found
        return {"error": "MRZ not found in the image"}
