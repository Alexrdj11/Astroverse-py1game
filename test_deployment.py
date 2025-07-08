#!/usr/bin/env python3
"""
Test script to verify deployment dependencies work
Run this before deploying to catch issues early
"""

try:
    print("Testing Flask...")
    import flask
    print(f"✅ Flask {flask.__version__} - OK")
    
    print("Testing Google Generative AI...")
    import google.generativeai as genai
    print("✅ Google Generative AI - OK")
    
    print("Testing python-dotenv...")
    import dotenv
    print("✅ Python-dotenv - OK")
    
    print("Testing app imports...")
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Test main app imports
    from app import app
    print("✅ App imports - OK")
    
    print("\n🎉 All deployment dependencies are working!")
    print("✅ Ready for deployment to Render.com")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Install missing packages with:")
    print("pip install Flask==2.3.3 google-generativeai==0.3.2 python-dotenv==1.0.0")
    
except Exception as e:
    print(f"❌ Error: {e}")
