import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_hf_comprehensive():
    """Comprehensive HuggingFace API test"""
    
    token = os.getenv('HF_TOKEN')
    print(f"🔍 Testing HuggingFace API Status")
    print(f"Token: {token[:15] if token else 'Not found'}...")
    print("-" * 50)
    
    if not token:
        print("❌ No HF_TOKEN found in environment")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test multiple endpoints
    endpoints = [
        "https://api-inference.huggingface.co/models/gpt2",
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small",
        "https://huggingface.co/api/whoami"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Testing: {endpoint}")
            
            if 'whoami' in endpoint:
                response = requests.get(endpoint, headers=headers, timeout=10)
            else:
                payload = {"inputs": "Hello", "parameters": {"max_new_tokens": 5}}
                response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ This endpoint is working!")
            elif response.status_code == 503:
                print("⚠️ Model loading but service available")
            else:
                print("❌ This endpoint has issues")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_hf_comprehensive()
