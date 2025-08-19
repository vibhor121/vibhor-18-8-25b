#!/bin/bash

echo "🔍 Deployment Readiness Check"
echo "================================"

# Check if required files exist
echo "📁 Checking deployment files..."

files=(
    ".gitignore"
    "backend/requirements.txt"
    "backend/main.py"
    "frontend/package.json"
    "render.yaml"
    "Procfile"
    "frontend/netlify.toml"
    "DEPLOYMENT_GUIDE.md"
)

missing_files=()
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        missing_files+=("$file")
    fi
done

echo ""
echo "🔧 Checking backend dependencies..."
cd backend
if python -m pip check; then
    echo "✅ Backend dependencies are compatible"
else
    echo "⚠️  Some backend dependency issues found"
fi
cd ..

echo ""
echo "🔧 Checking frontend dependencies..."
cd frontend
if npm audit --audit-level=high; then
    echo "✅ Frontend dependencies look good"
else
    echo "⚠️  Some frontend vulnerabilities found (check npm audit)"
fi
cd ..

echo ""
echo "📋 Pre-deployment checklist:"
echo "1. ✅ Create MongoDB Atlas cluster and get connection string"
echo "2. ✅ Push code to GitHub repository"
echo "3. ⏳ Deploy backend to Render with environment variables"
echo "4. ⏳ Deploy frontend to Netlify with VITE_API_URL"
echo "5. ⏳ Test the deployed application"

if [ ${#missing_files[@]} -eq 0 ]; then
    echo ""
    echo "🎉 All deployment files are ready!"
    echo "📖 Follow the DEPLOYMENT_GUIDE.md for step-by-step instructions."
else
    echo ""
    echo "❌ Please create the missing files before deploying."
fi 