# Todo App

A full-stack todo application built with React (Vite) frontend, FastAPI backend, and MongoDB database. Features user authentication with password hashing and complete CRUD operations for todos.

## Features

- 🔐 **User Authentication** - Register/Login with JWT tokens
- 🔒 **Password Hashing** - Secure password storage using bcrypt
- ✅ **CRUD Operations** - Create, Read, Update, Delete todos
- 👤 **User-specific Todos** - Each user sees only their own todos
- 🎨 **Modern UI** - Beautiful, responsive interface with Tailwind CSS
- 🚀 **Fast Backend** - High-performance FastAPI with async/await
- 📱 **Responsive Design** - Works on desktop and mobile devices

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for Python
- **MongoDB** - NoSQL database with PyMongo driver
- **JWT Authentication** - Secure token-based authentication
- **Bcrypt** - Password hashing
- **Pydantic** - Data validation

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and development server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Tailwind CSS** - Utility-first CSS framework
- **Heroicons** - Beautiful SVG icons

### Database
- **MongoDB** - Document database
- **Collections**: `users`, `todos`
- **Database**: `todoapp1`

## Prerequisites

Before running this application, make sure you have:

- Python 3.8+
- Node.js 16+
- MongoDB running on localhost:27017
- Git

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd todo-app
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env file with your configurations
```

**Environment Variables** (create `.env` file):
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=todoapp1
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

### 4. Database Setup

Make sure MongoDB is running on your system. The application will automatically create the required database (`todoapp1`) and collections (`users`, `todos`) when you first run it.

## Running the Application

### Start Backend Server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```
The backend will be available at: `http://localhost:8000`

### Start Frontend Server
```bash
cd frontend
npm run dev
```
The frontend will be available at: `http://localhost:3000`

## API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Authentication
- `POST /register` - Register new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user info

#### Todos
- `GET /todos` - Get all user's todos
- `POST /todos` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

## Usage

1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Add Todos**: Create new todos with title and optional description
4. **Manage Todos**: 
   - Mark as complete/incomplete
   - Edit title and description
   - Delete todos
5. **Logout**: Securely sign out

## Project Structure

```
todo-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── TodoList.jsx
│   │   ├── App.jsx         # Main app component
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   └── index.html          # HTML template
└── README.md               # This file
```

## Development

### Backend Development
- The FastAPI server supports hot reloading
- API documentation is automatically updated
- Use `uvicorn main:app --reload` for development

### Frontend Development
- Vite provides fast hot module replacement
- Use `npm run dev` for development server
- Build production version with `npm run build`

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Tokens**: Secure authentication with expiring tokens
- **Protected Routes**: API endpoints require authentication
- **CORS**: Properly configured for cross-origin requests
- **Input Validation**: Pydantic models validate all inputs

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running on localhost:27017
   - Check if the database service is started

2. **CORS Errors**
   - Make sure the frontend is running on port 3000
   - Check CORS configuration in backend/main.py

3. **Authentication Issues**
   - Clear browser localStorage and cookies
   - Check if JWT token has expired

4. **Module Import Errors**
   - Ensure all dependencies are installed
   - Activate virtual environment for backend

### Logs
- Backend logs: Check terminal where FastAPI is running
- Frontend logs: Open browser developer console
- MongoDB logs: Check MongoDB service logs 