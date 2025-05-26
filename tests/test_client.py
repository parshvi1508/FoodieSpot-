"""Test LLM functionality"""
import sys
import os

# Add project root to Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from ai.llm_client import LLMClient  # Now this will work

def test_llm():
    """Test LLM client with debugging"""
    print("[DEBUG] Testing LLM functionality...")
    
    print("🤖 LLM Client Test:")
    print("-" * 30)
    
    try:
        # Initialize client
        print("[DEBUG] Creating LLM client...")
        client = LLMClient()
        print("✅ LLM client created successfully")
        
        # Test simple response
        print("[DEBUG] Testing simple response...")
        response = client.get_response("Hello, how are you?")
        print(f"✅ LLM response received: '{response}'")
        
        # Test restaurant-related response
        print("[DEBUG] Testing restaurant-related response...")
        restaurant_response = client.get_response("Show me Italian restaurants")
        print(f"✅ Restaurant response: '{restaurant_response}'")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_llm()
    print(f"\n🎯 LLM test: {'PASSED' if success else 'FAILED'}")
