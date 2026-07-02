from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import sqlite3
from app.infrastructure.security.jwt import create_access_token

router = APIRouter()

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to prevent SQLite threading errors
def get_db_connection():
    # check_same_thread=False is critical for FastAPI with SQLite
    return sqlite3.connect("users.db", check_same_thread=False)

@router.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"DEBUG [REGISTER]: Attempting to register '{form_data.username}'...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password
        hashed_pw = pwd_context.hash(form_data.password)
        print("DEBUG [REGISTER]: Password hashed successfully.")
        
        # Insert into database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (form_data.username, hashed_pw))
        conn.commit()
        print("DEBUG [REGISTER]: Saved to database successfully.")
        
        return {"message": "User registered successfully"}
        
    except sqlite3.IntegrityError:
        print("DEBUG [REGISTER]: FAILED - Username already exists.")
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        print(f"DEBUG [REGISTER]: CRITICAL ERROR - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        conn.close()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"DEBUG [LOGIN]: Attempting to log in '{form_data.username}'...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (form_data.username,))
        user = cursor.fetchone()
        
        if not user:
            print("DEBUG [LOGIN]: FAILED - User not found.")
            raise HTTPException(status_code=401, detail="Invalid username or password")
            
        if not pwd_context.verify(form_data.password, user[0]):
            print("DEBUG [LOGIN]: FAILED - Password mismatch.")
            raise HTTPException(status_code=401, detail="Invalid username or password")
            
        print("DEBUG [LOGIN]: Success! Generating token.")
        return {"access_token": create_access_token(data={"sub": form_data.username}), "token_type": "bearer"}
        
    except Exception as e:
        print(f"DEBUG [REGISTER]: CRITICAL ERROR - {str(e)}")
        # CHANGE THE LINE BELOW:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()