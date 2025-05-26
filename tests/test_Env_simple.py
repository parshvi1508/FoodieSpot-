import os

print("=== Environment Test ===")

# Method 1: Check if already in environment
hf_token_direct = os.getenv('HF_TOKEN')
print(f"Direct check: {hf_token_direct}")

# Method 2: Try loading dotenv
try:
    from dotenv import load_dotenv
    print("✅ dotenv module available")
    
    # Load .env file
    result = load_dotenv()
    print(f"load_dotenv() result: {result}")
    
    # Check again
    hf_token_after = os.getenv('HF_TOKEN')
    print(f"After load_dotenv: {hf_token_after}")
    
except ImportError:
    print("❌ dotenv module not installed")
    print("Run: pip install python-dotenv")

# Method 3: Manual file reading
print("\n=== Manual .env file check ===")
try:
    with open('.env', 'r') as f:
        content = f.read().strip()
    print(f".env file content: '{content}'")
    
    # Extract token manually
    if 'HF_TOKEN=' in content:
        token = content.split('HF_TOKEN=')[1].split('\n')[0].strip()
        print(f"Extracted token: {token[:15]}...")
        
        # Set manually
        os.environ['HF_TOKEN'] = token
        print(f"Manually set token: {os.getenv('HF_TOKEN')[:15]}...")
        
except FileNotFoundError:
    print("❌ .env file not found in current directory")
    print(f"Current directory: {os.getcwd()}")

print(f"\n=== Final Status ===")
final_token = os.getenv('HF_TOKEN')
print(f"HF_TOKEN available: {bool(final_token)}")
if final_token:
    print(f"Token: {final_token[:15]}...")
