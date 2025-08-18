# Quick Start Guide

Get your Todo App running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB running on localhost:27017

## Setup (One-time)

```bash
# Make scripts executable (Linux/macOS)
chmod +x *.sh

# Run automated setup
./setup.sh
```

**Or manually:**

```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=todoapp1
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30" > .env

# Frontend setup
cd ../frontend
npm install
```

## Running the App

### Option 1: Using Scripts (Linux/macOS)
```bash
# Terminal 1 - Backend
./start-backend.sh

# Terminal 2 - Frontend  
./start-frontend.sh
```

### Option 2: Manual
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Access the App

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## First Steps

1. Open http://localhost:3000
2. Click "create a new account"
3. Register with username, email, password
4. Login and start creating todos!

## Troubleshooting

**MongoDB not running?**
```bash
# Start MongoDB (Linux)
sudo systemctl start mongod

# Or using Docker
docker run -d -p 27017:27017 mongo:latest
```

**Port already in use?**
- Backend: Change port in `backend/main.py`
- Frontend: Change port in `frontend/vite.config.js`

That's it! 🎉 