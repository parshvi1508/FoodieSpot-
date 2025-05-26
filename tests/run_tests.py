"""Run all tests with debugging"""
import sys
import os

# Add project root to Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.test_env import test_environment
from tests.test_client import test_llm
from tests.test_agent import test_agent

def run_all_tests():
    """Run complete test suite with debugging"""
    print("[DEBUG] Starting complete test suite...")
    print("🧪 FoodieSpot Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment),
        ("LLM Client", test_llm),
        ("Restaurant Agent", test_agent),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"🎯 {test_name}: {status}")
        except Exception as e:
            print(f"❌ {test_name}: FAILED with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("-" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready.")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()
