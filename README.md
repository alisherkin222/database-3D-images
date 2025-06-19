# 3D Printer Defect Image Uploader API

This project provides a FastAPI-based backend service for uploading and storing images of 3D printing defects. It supports metadata tagging and organizes the uploaded data into a structured PostgreSQL database for future machine learning, monitoring, or analysis tasks.

## Features

- Upload images of 3D print failures
- Store image metadata: material, temperature, printer model, defect type, speed, notes
- Automatic saving to local `uploads/` directory
- PostgreSQL support via SQLAlchemy
- FastAPI-based RESTful interface

##  Project Structure
How to Run

1. Install dependencies 

```bash pip install -r requirements.txt```

2. Create databse

```psql -U <your_user> -d <your_db> -f app/models.sql```

3. Set your DB credentials in database.py:

```DATABASE_URL = "postgresql://<user>:<password>@localhost/<db>"```

4. Run the API server

```uvicorn app.main:app --reload```

## API Example (Swagger)

You can test file upload directly via the built-in Swagger documentation at 
/docs. POST /upload/

- file: Upload image

- defect_type: (string)

- material: (string)

- printer_model: (string)

- temperature: (int)

- speed: (int)

- notes: (optional)


