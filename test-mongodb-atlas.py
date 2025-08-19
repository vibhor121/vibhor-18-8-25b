#!/usr/bin/env python3
"""
MongoDB Atlas Connection Test Script
Usage: python test-mongodb-atlas.py
"""

import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    
    # Load environment variables from backend/.env
    backend_env = os.path.join(os.path.dirname(__file__), 'backend', '.env')
    if os.path.exists(backend_env):
        load_dotenv(backend_env)
        print(f"📁 Loading environment from: {backend_env}")
    else:
        load_dotenv()  # Try current directory
    
    # Get MongoDB URL from environment
    mongodb_url = os.getenv("MONGODB_URL")
    
    if not mongodb_url:
        print("❌ MONGODB_URL environment variable not set")
        print("💡 Create a .env file in the backend directory with your MongoDB Atlas connection string")
        print("   Example: MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority")
        return False
    
    if mongodb_url == "mongodb://localhost:27017":
        print("⚠️  Using local MongoDB URL. For production, use MongoDB Atlas connection string.")
        
    try:
        print("🔗 Attempting to connect to MongoDB...")
        print(f"🔗 URL: {mongodb_url[:50]}..." if len(mongodb_url) > 50 else mongodb_url)
        
        # Create MongoDB client
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        
        print("✅ Successfully connected to MongoDB!")
        
        # Test database operations
        db_name = os.getenv("DATABASE_NAME", "todoapp1")
        db = client[db_name]
        
        # Test write operation
        test_collection = db.test_connection
        result = test_collection.insert_one({"test": "connection", "timestamp": "2024"})
        print(f"✅ Test write successful. Document ID: {result.inserted_id}")
        
        # Test read operation
        document = test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Test read successful. Document: {document}")
        
        # Cleanup test document
        test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test cleanup successful")
        
        # Get database stats
        stats = db.command("dbstats")
        print(f"📊 Database: {db_name}")
        print(f"📊 Collections: {stats.get('collections', 'N/A')}")
        print(f"📊 Data Size: {stats.get('dataSize', 'N/A')} bytes")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your MongoDB Atlas connection string")
        print("2. Ensure your IP address is whitelisted in Atlas")
        print("3. Verify username and password are correct")
        print("4. Check if the cluster is running")
        return False

if __name__ == "__main__":
    print("🧪 MongoDB Atlas Connection Test")
    print("=" * 40)
    
    success = test_mongodb_connection()
    
    if success:
        print("\n🎉 Your MongoDB Atlas connection is ready for deployment!")
    else:
        print("\n❌ Please fix the MongoDB connection before deploying")
        sys.exit(1) 