CREATE TABLE defects (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    defect_type TEXT NOT NULL,
    material TEXT,
    printer_model TEXT,
    temperature INT,
    speed INT,
    captured_at TIMESTAMP DEFAULT now(),
    notes TEXT,
    storage_url TEXT
);
