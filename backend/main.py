from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import os
import ssl
import sqlite3
import json
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, Field, ConfigDict

# Load environment variables
load_dotenv()

# Database configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "todoapp1")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Initialize FastAPI app
app = FastAPI(title="Todo App API", version="1.0.0")

# CORS middleware - Updated for production
allowed_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "https://*.netlify.app",
    "https://*.onrender.com"
]

# In production, you should replace the wildcards with your actual domains
if ENVIRONMENT == "production":
    # Add your actual production domains here
    allowed_origins.extend([
        "https://vibhor-todo-app.netlify.app",
        "https://amazing-gaufre-*.netlify.app",  # Netlify auto-generated names
        # Add your custom Netlify domain here once you get it
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.netlify\.app|https://.*\.onrender\.com|http://localhost:3000|http://127\.0\.0\.1:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration and connection
USE_MONGODB = True
USE_SQLITE = False

# Try MongoDB first
try:
    client = MongoClient(
        MONGODB_URL,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=10,
        retryWrites=True,
        w='majority'
    )
    db = client[DATABASE_NAME]
    users_collection = db.users
    todos_collection = db.todos
    
    # Test connection
    client.admin.command('ping')
    print(f"✅ Connected to MongoDB Atlas successfully!")
    USE_MONGODB = True
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)}")
    print("🔄 Falling back to SQLite database...")
    
    # Fallback to SQLite
    USE_MONGODB = False
    USE_SQLITE = True
    
    # Create SQLite database
    sqlite_conn = sqlite3.connect('/tmp/todoapp.db', check_same_thread=False)
    sqlite_conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    sqlite_conn.execute('''CREATE TABLE IF NOT EXISTS todos (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,
        created_at TEXT NOT NULL,
        user_id TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    sqlite_conn.commit()
    print("✅ SQLite database initialized successfully!")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    user_id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    return get_user_by_username(username)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    try:
        # Check if user already exists
        if check_user_exists(username=user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if check_user_exists(email=user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user.password)
        user_doc = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password,
            "created_at": datetime.now(timezone.utc)
        }
        
        created_user = create_user(user_doc)
        created_user["id"] = created_user["_id"]
        
        return UserResponse(**created_user)
    except HTTPException:
        # Re-raise HTTP exceptions (user already exists, etc.)
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    user_response = current_user.copy()
    user_response["id"] = str(user_response["_id"])
    del user_response["_id"]
    return UserResponse(**user_response)

@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, current_user: dict = Depends(get_current_user)):
    todo_doc = {
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": datetime.now(timezone.utc),
        "user_id": current_user["_id"]
    }
    
    result = todos_collection.insert_one(todo_doc)
    todo_doc["id"] = str(result.inserted_id)
    del todo_doc["_id"]  # Remove _id field
    
    return TodoResponse(**todo_doc)

@app.get("/todos", response_model=List[TodoResponse])
async def get_todos(current_user: dict = Depends(get_current_user)):
    todos = list(todos_collection.find({"user_id": current_user["_id"]}))
    for todo in todos:
        todo["id"] = str(todo["_id"])
        del todo["_id"]
    return [TodoResponse(**todo) for todo in todos]

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: str, current_user: dict = Depends(get_current_user)):
    try:
        todo = todos_collection.find_one({
            "_id": ObjectId(todo_id),
            "user_id": current_user["_id"]
        })
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        todo["id"] = str(todo["_id"])
        del todo["_id"]
        return TodoResponse(**todo)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid todo ID")

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str, 
    todo_update: TodoUpdate, 
    current_user: dict = Depends(get_current_user)
):
    try:
        update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        result = todos_collection.update_one(
            {"_id": ObjectId(todo_id), "user_id": current_user["_id"]},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        updated_todo = todos_collection.find_one({
            "_id": ObjectId(todo_id),
            "user_id": current_user["_id"]
        })
        updated_todo["id"] = str(updated_todo["_id"])
        del updated_todo["_id"]
        
        return TodoResponse(**updated_todo)
    except Exception as e:
        if "Todo not found" in str(e):
            raise e
        raise HTTPException(status_code=400, detail="Invalid todo ID")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, current_user: dict = Depends(get_current_user)):
    try:
        result = todos_collection.delete_one({
            "_id": ObjectId(todo_id),
            "user_id": current_user["_id"]
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        if "Todo not found" in str(e):
            raise e
        raise HTTPException(status_code=400, detail="Invalid todo ID")

@app.get("/")
async def root():
    return {"message": "Todo App API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint to test database connectivity"""
    try:
        if USE_MONGODB:
            # Test MongoDB connection
            client.admin.command('ping')
            db_stats = db.command("dbstats")
            
            return {
                "status": "healthy",
                "database": "mongodb",
                "connected": True,
                "database_name": DATABASE_NAME,
                "environment": ENVIRONMENT,
                "collections": db_stats.get("collections", 0)
            }
        else:
            # Test SQLite connection
            cursor = sqlite_conn.execute('SELECT COUNT(*) FROM users')
            user_count = cursor.fetchone()[0]
            
            return {
                "status": "healthy", 
                "database": "sqlite",
                "connected": True,
                "database_name": "todoapp.db",
                "environment": ENVIRONMENT,
                "user_count": user_count
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "mongodb" if USE_MONGODB else "sqlite",
            "connected": False,
            "error": str(e),
            "database_name": DATABASE_NAME if USE_MONGODB else "todoapp.db",
            "environment": ENVIRONMENT
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 