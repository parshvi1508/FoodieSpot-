import os
from pathlib import Path
from dotenv import load_dotenv

print("🔍 Advanced Environment Variable Debug:")
print("-" * 50)

# Check current directory
current_dir = Path.cwd()
print(f"📁 Current directory: {current_dir}")

# Check if .env file exists
env_file = current_dir / ".env"
print(f"📄 .env file path: {env_file}")
print(f"📄 .env file exists: {env_file.exists()}")

if env_file.exists():
    print(f"📄 .env file size: {env_file.stat().st_size} bytes")
    
    # Read .env file content
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        print(f"📄 .env file content:")
        print(repr(content))  # Shows exact content including hidden characters
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")

# Test load_dotenv with explicit path
print(f"\n🔍 Testing load_dotenv...")
try:
    result = load_dotenv(env_file)
    print(f"✅ load_dotenv result: {result}")
except Exception as e:
    print(f"❌ load_dotenv error: {e}")

# Check environment variables
print(f"\n🔍 Environment Variables:")
hf_token = os.getenv('HF_TOKEN')
print(f"✅ HF_TOKEN: {hf_token}")

# Check all environment variables containing 'HF' or 'TOKEN'
print(f"\n🔍 All HF/TOKEN related env vars:")
for key, value in os.environ.items():
    if 'HF' in key.upper() or 'TOKEN' in key.upper():
        print(f"  {key}: {value[:15] if value else 'None'}...")

# Test manual loading
print(f"\n🔍 Manual .env parsing:")
if env_file.exists():
    try:
        with open(env_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        print(f"  Line {line_num}: {key} = {value[:15]}...")
                        os.environ[key] = value  # Set manually
                    else:
                        print(f"  Line {line_num}: Invalid format: {line}")
        
        # Test after manual loading
        manual_token = os.getenv('HF_TOKEN')
        print(f"🎯 After manual loading - HF_TOKEN: {manual_token[:15] if manual_token else 'None'}...")
        
    except Exception as e:
        print(f"❌ Manual parsing error: {e}")
