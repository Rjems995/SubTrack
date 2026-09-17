import sqlite3
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI Application
app = FastAPI(title="SubTrack API", description="Backend API for SubTrack Subscription Manager")

# Enable CORS (Cross-Origin Resource Sharing) so index.html can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Helper
DB_NAME = "subtrack.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Database Initialization
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            cycle TEXT,
            cost REAL NOT NULL,
            nextDate TEXT,
            paymentMethod TEXT,
            status TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

# Run database setup on startup
init_db()

# Pydantic Data Models for Request & Response validation
class Subscription(BaseModel):
    id: str
    name: str
    category: Optional[str] = "Other"
    cycle: Optional[str] = "Monthly"
    cost: float
    nextDate: Optional[str] = ""
    paymentMethod: Optional[str] = ""
    status: Optional[str] = "Active"
    notes: Optional[str] = ""

# API Endpoints

@app.get("/")
def root():
    return {"message": "SubTrack API is running!"}

@app.get("/api/subscriptions", response_model=List[Subscription])
def get_all_subscriptions():
    """Retrieve all subscriptions from the SQLite database."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM subscriptions").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/subscriptions", response_model=Subscription)
def create_subscription(sub: Subscription):
    """Save a new subscription into the database."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO subscriptions (id, name, category, cycle, cost, nextDate, paymentMethod, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sub.id, sub.name, sub.category, sub.cycle, sub.cost, sub.nextDate, sub.paymentMethod, sub.status, sub.notes))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Subscription ID already exists")
    conn.close()
    return sub

@app.put("/api/subscriptions/{sub_id}", response_model=Subscription)
def update_subscription(sub_id: str, sub: Subscription):
    """Update an existing subscription in the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE subscriptions 
        SET name = ?, category = ?, cycle = ?, cost = ?, nextDate = ?, paymentMethod = ?, status = ?, notes = ?
        WHERE id = ?
    """, (sub.name, sub.category, sub.cycle, sub.cost, sub.nextDate, sub.paymentMethod, sub.status, sub.notes, sub_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    conn.commit()
    conn.close()
    return sub

@app.delete("/api/subscriptions/{sub_id}")
def delete_subscription(sub_id: str):
    """Delete a subscription from the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    conn.commit()
    conn.close()
    return {"message": f"Subscription '{sub_id}' deleted successfully."}

# To run locally:
# 1. Install dependencies: pip install fastapi uvicorn
# 2. Start server: uvicorn main:app --reload