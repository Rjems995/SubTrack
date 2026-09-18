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

# Database Initialization with Schema and Default Seeding
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'Other',
            cycle TEXT DEFAULT 'Monthly',
            cost REAL NOT NULL,
            nextDate TEXT,
            paymentMethod TEXT,
            status TEXT DEFAULT 'Active',
            isTrial INTEGER DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Create indexes for optimized queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON subscriptions(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON subscriptions(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_nextDate ON subscriptions(nextDate)")
    
    # Seed initial database entries if empty
    cursor.execute("SELECT COUNT(*) as count FROM subscriptions")
    if cursor.fetchone()["count"] == 0:
        sample_data = [
            ("sub-1", "Netflix Premium", "Entertainment", "Monthly", 19.99, "2026-10-05", "Visa ...4242", "Active", 0, "4K UHD Family Account"),
            ("sub-2", "ChatGPT Plus", "Productivity", "Monthly", 20.00, "2026-10-12", "Mastercard", "Active", 0, "AI Assistant"),
            ("sub-3", "Spotify Duo", "Entertainment", "Monthly", 14.99, "2026-10-02", "PayPal", "Active", 0, "Music streaming"),
            ("sub-4", "Adobe CC Trial", "Software/SaaS", "Monthly", 54.99, "2026-10-03", "Visa", "Active", 1, "7-Day Promotional Trial"),
            ("sub-5", "Gym Membership", "Health/Fitness", "Monthly", 45.00, "2026-10-20", "Debit Card", "Paused", 0, "Fitness club access")
        ]
        cursor.executemany("""
            INSERT INTO subscriptions (id, name, category, cycle, cost, nextDate, paymentMethod, status, isTrial, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        
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
    isTrial: Optional[bool] = False
    notes: Optional[str] = ""

# API Endpoints

@app.get("/")
def root():
    return {"message": "SubTrack API is running with SQLite database support!"}

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
            INSERT INTO subscriptions (id, name, category, cycle, cost, nextDate, paymentMethod, status, isTrial, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (sub.id, sub.name, sub.category, sub.cycle, sub.cost, sub.nextDate, sub.paymentMethod, sub.status, 1 if sub.isTrial else 0, sub.notes))
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
        SET name = ?, category = ?, cycle = ?, cost = ?, nextDate = ?, paymentMethod = ?, status = ?, isTrial = ?, notes = ?
        WHERE id = ?
    """, (sub.name, sub.category, sub.cycle, sub.cost, sub.nextDate, sub.paymentMethod, sub.status, 1 if sub.isTrial else 0, sub.notes, sub_id))
    
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
