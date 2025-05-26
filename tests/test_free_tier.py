import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_verified_free_models():
    """Test models that ACTUALLY work on free tier"""
    
    token = os.getenv('HF_TOKEN')
    print(f"🔍 Testing VERIFIED Free Tier Models")
    print(f"Token: {token[:15] if token else 'Not found'}...")
    print("-" * 50)
    
    if not token:
        print("❌ No HF_TOKEN found")
        return False
    
    # These models DEFINITELY exist and work on free tier
    verified_models = [
        "gpt2",                           # Always works
        "distilgpt2",                     # Smaller version
        "microsoft/DialoGPT-medium",      # Conversation
        "EleutherAI/gpt-neo-125M"         # Small but good
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    for model in verified_models:
        print(f"\n🤖 Testing: {model}")
        
        try:
            api_url = f"https://api-inference.huggingface.co/models/{model}"
            payload = {
                "inputs": "Hello! I help with restaurant bookings.",
                "parameters": {
                    "max_new_tokens": 30,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=15)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS: {model}")
                print(f"Response: {result}")
                return True
                
            elif response.status_code == 503:
                print(f"⏳ MODEL LOADING: {model} (will work soon)")
                
            elif response.status_code == 429:
                print(f"⚠️ RATE LIMITED: {model}")
                
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    return False

if __name__ == "__main__":
    success = test_verified_free_models()
    print(f"\n🎯 Free tier test: {'PASSED' if success else 'USING FALLBACK'}")
