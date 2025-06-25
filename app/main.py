
# === app/database.py ===
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.database import get_connection
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

app = FastAPI()


# CORS (чтобы можно было обращаться с других устройств)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для тестов разрешаем всё
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Defect(BaseModel):
    id: int
    filename: str
    defect_type: str
    material: str = None
    printer_model: str = None
    temperature: int = None
    speed: int = None
    notes: str = None
    storage_url: str

@app.post("/upload/", response_model=Defect)
async def upload(
    file: UploadFile = File(...),
    defect_type: str = Form(...),
    material: str = Form(None),
    printer_model: str = Form(None),
    temperature: int = Form(None),
    speed: int = Form(None),
    notes: str = Form(None)
):
    filename = file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    storage_url = f"/uploads/{filename}"

    conn = await get_connection()
    await conn.execute("""
           INSERT INTO defects (filename, defect_type, material, printer_model, temperature, speed, notes, storage_url)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       """, filename, defect_type, material, printer_model, temperature, speed, notes, storage_url)
    await conn.close()

    # Возвращаем инфу клиенту
    return {"status": "ok", "file_saved_as": filename, "url": storage_url}


@app.get("/defects/", response_model=List[Defect])
async def get_defects():
    conn = await get_connection()
    records = await conn.fetch("SELECT * FROM defects")
    await conn.close()
    return [dict(r) for r in records]

@app.get("/defects/{defect_id}", response_model=Defect)
async def get_defect(defect_id: int):
    conn = await get_connection()
    record = await conn.fetchrow("SELECT * FROM defects WHERE id = $1", defect_id)
    await conn.close()
    if not record:
        raise HTTPException(status_code=404, detail="Defect not found")
    return dict(record)

@app.delete("/defects/{defect_id}")
async def delete_defect(defect_id: int):
    conn = await get_connection()
    deleted = await conn.execute("DELETE FROM defects WHERE id = $1", defect_id)
    await conn.close()
    return {"status": "deleted", "id": defect_id}

@app.get("/get_image/{filename}")
def get_image(filename: str):
    file_path = f"./uploads/{filename}"
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path, media_type="image/jpeg")

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")




