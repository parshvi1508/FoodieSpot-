"""Test AI agent"""
import sys
import os

# Add project root to Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from ai.agent import RestaurantAgent

def test_agent():
    """Test restaurant agent with debugging"""
    print("[DEBUG] Testing Restaurant Agent...")
    
    print("🎯 Restaurant Agent Test:")
    print("-" * 30)
    
    try:
        # Initialize agent
        print("[DEBUG] Creating Restaurant agent...")
        agent = RestaurantAgent()
        print("✅ Agent created successfully")
        
        # Test chat
        print("[DEBUG] Testing agent chat...")
        response = agent.chat("Show me Italian restaurants")
        print(f"✅ Agent response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_agent()
    print(f"\n🎯 Agent test: {'PASSED' if success else 'FAILED'}")
