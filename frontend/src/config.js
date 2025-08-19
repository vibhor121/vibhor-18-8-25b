// API Configuration
const config = {
  // Use environment variable for API URL, fallback to localhost for development
  API_BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  
  // Other configuration options
  APP_NAME: 'Todo App',
  VERSION: '1.0.0'
}

export default config 