#!/usr/bin/env python3
"""
Script to create the .env file for the Todo App backend
"""

import secrets
import os

def create_env_file():
    env_content = f"""MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=todoapp1
SECRET_KEY={secrets.token_hex(32)}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("📝 You can edit the .env file to customize your configuration.")

if __name__ == "__main__":
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Aborted. Keeping existing .env file.")
            exit(0)
    
    create_env_file() 