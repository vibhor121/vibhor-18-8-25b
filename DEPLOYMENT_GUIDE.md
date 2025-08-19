# 🚀 Deployment Guide

## Overview
This guide will help you deploy your Todo App to production using:
- **MongoDB Atlas** - Cloud database
- **Render** - Backend API hosting
- **Netlify** - Frontend hosting

## 📝 Prerequisites
- GitHub account
- MongoDB Atlas account (free tier available)
- Render account (free tier available)
- Netlify account (free tier available)

---

## 🗄️ Step 1: Setup MongoDB Atlas

### 1.1 Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account
3. Create a new cluster (choose free tier M0)

### 1.2 Configure Database Access
1. Go to **Database Access** in your Atlas dashboard
2. Click **Add New Database User**
3. Choose **Password** authentication
4. Username: `todoapp` (or your choice)
5. Password: Generate a secure password (save this!)
6. Database User Privileges: **Read and write to any database**
7. Click **Add User**

### 1.3 Configure Network Access
1. Go to **Network Access**
2. Click **Add IP Address**
3. Choose **Allow Access from Anywhere** (0.0.0.0/0)
4. Click **Confirm**

### 1.4 Get Connection String
1. Go to **Clusters** and click **Connect**
2. Choose **Connect your application**
3. Select **Python** and **4.0 or later**
4. Copy the connection string (it will look like):
   ```
   mongodb+srv://todoapp:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password
6. Save this connection string - you'll need it for Render deployment

---

## 🖥️ Step 2: Deploy Backend to Render

### 2.1 Prepare for Render Deployment
The following files have been created for you:
- `render.yaml` - Render service configuration
- `Procfile` - Process file for Render
- Updated environment configuration

### 2.2 Deploy to Render
1. Push your code to GitHub (make sure .gitignore excludes sensitive files)
2. Go to [Render](https://render.com) and sign up/login
3. Click **New** → **Web Service**
4. Connect your GitHub repository
5. Use these settings:
   - **Name**: `todo-app-backend` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Auto-Deploy**: Yes

### 2.3 Set Environment Variables in Render
1. In your Render service dashboard, go to **Environment**
2. Add these environment variables:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: A secure random string (generate one)
   - `DATABASE_NAME`: `todoapp1`
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

### 2.4 Get Your Backend URL
After deployment, Render will provide a URL like:
`https://todo-app-backend.onrender.com`

---

## 🌐 Step 3: Deploy Frontend to Netlify

### 3.1 Update Frontend Configuration
The frontend needs to know your backend URL. This will be updated automatically.

### 3.2 Deploy to Netlify
1. Go to [Netlify](https://netlify.com) and sign up/login
2. Click **Add new site** → **Import an existing project**
3. Connect to GitHub and select your repository
4. Use these settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
5. Click **Deploy site**

### 3.3 Set Environment Variables in Netlify
1. In your Netlify site dashboard, go to **Site settings** → **Environment variables**
2. Add:
   - `VITE_API_URL`: Your Render backend URL (e.g., `https://todo-app-backend.onrender.com`)

### 3.4 Redeploy
After setting environment variables, trigger a new deployment.

---

## ✅ Step 4: Verify Deployment

1. **Frontend**: Your Netlify URL (e.g., `https://your-app.netlify.app`)
2. **Backend API**: Your Render URL + `/docs` (e.g., `https://todo-app-backend.onrender.com/docs`)
3. **Database**: Check MongoDB Atlas dashboard for connections

---

## 🔧 Troubleshooting

### Common Issues:
1. **CORS errors**: Make sure your Render URL is added to CORS origins in backend
2. **Database connection**: Verify MongoDB Atlas connection string and IP whitelist
3. **Environment variables**: Double-check all environment variables are set correctly
4. **Build failures**: Check build logs in Render/Netlify dashboards

### Useful Commands:
```bash
# Test backend locally with production database
export MONGODB_URL="your-atlas-connection-string"
python backend/main.py

# Test frontend build
cd frontend && npm run build
```

---

## 💡 Production Tips

1. **Security**: Use strong passwords and rotate secrets regularly
2. **Monitoring**: Set up alerts in MongoDB Atlas and Render
3. **Backups**: MongoDB Atlas provides automatic backups
4. **Custom Domain**: You can add custom domains in both Render and Netlify
5. **SSL**: Both platforms provide free SSL certificates

---

## 📞 Support

If you encounter issues:
1. Check the deployment logs in Render/Netlify
2. Verify MongoDB Atlas connection
3. Test API endpoints individually
4. Check browser console for frontend errors 