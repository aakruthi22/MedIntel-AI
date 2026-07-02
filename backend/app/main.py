from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth, research, documents
from app.db.database import init_db

# 1. Initialize the FastAPI app
app = FastAPI(title="MedIntel AI Backend")

# 2. Configure CORS
# This allows your Next.js frontend at localhost:3000 to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# 4. Include your routers
# We leave the prefix blank for auth so your frontend can call /register and /token directly.
# The research and documents routers keep their specific API prefixes.
app.include_router(auth.router, tags=["Authentication"])
app.include_router(research.router, prefix="/api/v1/research", tags=["Research"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])