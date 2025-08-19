// API Configuration
const config = {
  // Use environment variable for API URL, fallback to production URL
  API_BASE_URL: import.meta.env.VITE_API_URL || 'https://vibhor-18-8-25b.onrender.com',
  
  // Other configuration options
  APP_NAME: 'Todo App',
  VERSION: '1.0.0'
}

export default config 