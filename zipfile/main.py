from fastapi import FastAPI, File, UploadFile, HTTPException
import tempfile
import zipfile
import os

app = FastAPI()

@app.post("/upload/")
async def upload_and_extract(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_path = os.path.join(temp_dir, file.filename)
            with open(temp_zip_path, "wb") as temp_zip:
                temp_zip.write(await file.read())

            with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Walk through the directory to list all files
            extracted_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    extracted_files.append(os.path.relpath(os.path.join(root, file), temp_dir))

            return {"extracted_files": extracted_files}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
