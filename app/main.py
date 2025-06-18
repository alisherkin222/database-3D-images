from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    defect_type: str = Form(...),
    material: str = Form(None),
    printer_model: str = Form(None),
    temperature: int = Form(None),
    speed: int = Form(None),
    notes: str = Form(None)
):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"status": "uploaded", "filename": file.filename}
