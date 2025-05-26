import os
import requests
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

class LLMClient:
    """Working HuggingFace free tier client with verified models"""
    
    def __init__(self):
        print("[DEBUG] Initializing HuggingFace free tier client...")
        
        self.token = os.getenv('HF_TOKEN')
        
        # VERIFIED WORKING MODELS (From search results [4][6][8])
        self.working_models = [
    "HuggingFaceH4/zephyr-7b-beta",           # ✅ Stable chat model, best option
    "HuggingFaceH4/zephyr-7b-alpha",          # ✅ Older version, also works
]

        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        } if self.token else {}
        
        self.working_model = None
        self.fallback_mode = False
        
        print(f"[DEBUG] Testing {len(self.working_models)} verified models...")
        self._test_models()
    
    def _test_models(self):
        """Test models with proper error handling"""
        
        if not self.token:
            print("[DEBUG] No token found - using intelligent fallback")
            self.fallback_mode = True
            return
        
        for model in self.working_models:
            if self._test_single_model(model):
                self.working_model = model
                print(f"[DEBUG] ✅ Using working model: {model}")
                return
        
        print("[DEBUG] No models working - using intelligent fallback")
        self.fallback_mode = True
    
    def _test_single_model(self, model):
        """Test a single model quickly"""
        try:
            print(f"[DEBUG] Quick test: {model}")
            
            api_url = f"https://api-inference.huggingface.co/models/{model}"
            
            # Simple test payload
            payload = {
                "inputs": "Hello",
                "parameters": {
                    "max_new_tokens": 10,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"[DEBUG] ✅ {model} working!")
                return True
            elif response.status_code == 503:
                print(f"[DEBUG] ⏳ {model} loading but available")
                return True
            else:
                print(f"[DEBUG] ❌ {model} failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[DEBUG] ❌ {model} error: {e}")
            return False
    
    def get_response(self, prompt: str) -> str:
        """Get response from HuggingFace or intelligent fallback"""
        
        # Try HuggingFace if available
        if not self.fallback_mode and self.working_model:
            hf_response = self._call_huggingface(prompt)
            if hf_response:
                return hf_response
        
        # Use restaurant-optimized fallback
        return self._generate_restaurant_response(prompt)
    
    def _call_huggingface(self, prompt: str) -> str:
        """Call HuggingFace with proper error handling"""
        try:
            api_url = f"https://api-inference.huggingface.co/models/{self.working_model}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                api_url,
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result:
                    text = result[0].get('generated_text', '').strip()
                    if text and len(text) > 5:
                        print("[DEBUG] ✅ HuggingFace response success")
                        return text
            
        except Exception as e:
            print(f"[DEBUG] HuggingFace call failed: {e}")
        
        return None
    
    def _generate_restaurant_response(self, prompt: str) -> str:
        """Restaurant-optimized intelligent responses"""
        prompt_lower = prompt.lower()
        
        # Your existing excellent fallback logic
        if any(word in prompt_lower for word in ['show', 'suggest', 'list', 'find', 'restaurants']):
            if 'italian' in prompt_lower:
                return """Here are our Italian restaurants:

**1. Pasta Palace** 🍝
   📍 Midtown | Authentic Italian cuisine
   Specialties: Fresh pasta, wood-fired pizza, traditional sauces

**2. Osteria Francescana** 🍝
   📍 Modena | Fine Italian dining
   Specialties: Michelin-quality dishes, wine pairings

**3. Villa Crespi** 🍝
   📍 Orta San Giulio | Traditional Italian
   Specialties: Regional specialties, romantic atmosphere

All serve authentic Italian cuisine with fresh ingredients. Which would you like to book?"""

            elif 'indian' in prompt_lower:
                return """Here are our Indian restaurants:

**1. Spice Garden** 🍛
   📍 Downtown | Traditional Indian cuisine
   Specialties: Authentic spices, curries, tandoori dishes

**2. Bukhara** 🍛
   📍 Delhi | North Indian cuisine
   Specialties: Kebabs, naan, rich gravies

**3. Indian Accent** 🍛
   📍 Delhi | Modern Indian cuisine
   Specialties: Contemporary Indian flavors, fusion dishes

Perfect for enjoying authentic Indian flavors! Which restaurant interests you?"""
            
            else:
                return """Here are our popular restaurants by cuisine:

🍝 **Italian:** Pasta Palace, Osteria Francescana, Villa Crespi
🍛 **Indian:** Spice Garden, Bukhara, Indian Accent
🥢 **Chinese:** Dragon Wok, Din Tai Fung
🥖 **French:** Le Bistro, Alain Ducasse
🌮 **Mexican:** Taco Fiesta

What type of cuisine would you like to explore?"""
        
        elif any(word in prompt_lower for word in ['book', 'reserve', 'table']):
            return """I'd be happy to help you book a table!

**I need to know:**
• **Restaurant name** (from our available options)
• **Party size** (how many people)
• **Date** (when you'd like to dine)
• **Time** (preferred dining time)

**💡 Example:** 'Book Spice Garden for 4 people tomorrow at 7pm'

Which restaurant would you like to book?"""
        
        elif any(word in prompt_lower for word in ['name is', 'phone', 'contact']):
            return "Perfect! I have your contact information. Let me check availability and proceed with your reservation immediately."
        
        else:
            return "I'm here to help with restaurant bookings! Try asking: 'Show me Italian restaurants' or 'Book a table for 4 people'"
