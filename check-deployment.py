#!/usr/bin/env python3
"""
Deployment Status Checker
Tests backend and frontend endpoints after deployment
"""

import requests
import sys
import time

def check_backend(url):
    """Check if backend is responding"""
    try:
        print(f"🔗 Testing backend: {url}")
        
        # Test root endpoint
        response = requests.get(f"{url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Backend root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend root endpoint failed: {response.status_code}")
            return False
        
        # Test docs endpoint
        response = requests.get(f"{url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Backend docs endpoint working")
        else:
            print(f"⚠️  Backend docs endpoint: {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {str(e)}")
        return False

def check_frontend(url):
    """Check if frontend is responding"""
    try:
        print(f"🔗 Testing frontend: {url}")
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is responding")
            if "Todo App" in response.text or "Login" in response.text:
                print("✅ Frontend content looks correct")
            return True
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {str(e)}")
        return False

def main():
    print("🚀 Deployment Status Checker")
    print("=" * 50)
    
    # Get URLs from user or use examples
    backend_url = input("Enter your Render backend URL (or press Enter to skip): ").strip()
    frontend_url = input("Enter your Netlify frontend URL (or press Enter to skip): ").strip()
    
    results = []
    
    if backend_url:
        print("\n📡 Checking Backend...")
        backend_ok = check_backend(backend_url)
        results.append(("Backend", backend_ok))
    
    if frontend_url:
        print("\n🌐 Checking Frontend...")
        frontend_ok = check_frontend(frontend_url)
        results.append(("Frontend", frontend_ok))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Deployment Summary:")
    
    all_good = True
    for name, status in results:
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {name}: {'Working' if status else 'Failed'}")
        if not status:
            all_good = False
    
    if all_good and results:
        print("\n🎉 All services are working correctly!")
        print("🔗 Your Todo App is ready to use!")
    elif results:
        print("\n⚠️  Some services need attention. Check the logs above.")
    else:
        print("\n💡 No URLs provided to test.")
        print("   Run this script again when your deployment is ready.")

if __name__ == "__main__":
    main() 