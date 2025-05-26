"""Test environment setup"""
import sys
import os

# Add project root to Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from dotenv import load_dotenv

def test_environment():
    """Test environment variables with debugging"""
    print("[DEBUG] Testing environment setup...")
    load_dotenv()
    
    print("🔍 Environment Test Results:")
    print("-" * 40)
    
    # Check HF token
    hf_token = os.getenv('HF_TOKEN')
    print(f"✅ HF_TOKEN found: {bool(hf_token)}")
    
    if hf_token:
        print(f"✅ Token format: {hf_token[:15]}...")
        print(f"✅ Token length: {len(hf_token)}")
        print(f"✅ Starts with 'hf_': {hf_token.startswith('hf_')}")
        
        if len(hf_token) == 37 and hf_token.startswith('hf_'):
            print("✅ Token format looks correct!")
            return True
        else:
            print("❌ Token format may be incorrect")
            return False
    else:
        print("❌ No HF_TOKEN found in environment")
        return False

if __name__ == "__main__":
    success = test_environment()
    print(f"\n🎯 Environment test: {'PASSED' if success else 'FAILED'}")
