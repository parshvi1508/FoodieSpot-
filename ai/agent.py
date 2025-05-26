import json
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .llm_client import LLMClient
from .services import get_restaurants_ai, check_availability_ai, make_reservation_ai

from .recommendation_service import RecommendationService
load_dotenv()

class RestaurantAgent:
    """Fixed AI Agent with proper parsing and real-time updates"""
    
    def __init__(self):
        print("[DEBUG] Initializing Fixed Restaurant AI Agent...")
        
        # Initialize LLM client
        try:
            self.llm = LLMClient()
            print("[DEBUG] LLM client initialized successfully")
        except Exception as e:
            print(f"[DEBUG] LLM client initialization failed: {e}")
            raise
        
        # Reset conversation context properly
        self.reset_conversation()
        print("[DEBUG] Fixed Restaurant AI Agent ready")
        
    def chat(self, user_message: str) -> str:
        """Fixed chat with proper context management"""
        print(f"[DEBUG] User message: '{user_message}'")
        print(f"[DEBUG] Current step: {self.booking_context['current_step']}")
        
        try:
            # IMPORTANT: Check if this is a new conversation request
            if self._is_new_conversation_request(user_message):
                print("[DEBUG] Detected new conversation - resetting context")
                self.reset_conversation()
            
            # Update context with new information
            self._update_booking_context_fixed(user_message)
            
            # Enhanced intent classification
            intent = self._classify_intent_enhanced(user_message)
            print(f"[DEBUG] Classified intent: {intent}")
            
            # Execute based on intent
            response = self._handle_intent(intent, user_message)
            
            # Store conversation
            self.conversation.append({
                "user": user_message, 
                "agent": response,
                "intent": intent,
                "context_snapshot": self.booking_context.copy(),
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"[DEBUG] Final response: '{response}'")
            return response
            
        except Exception as e:
            print(f"[DEBUG] Chat error: {e}")
            return "I'm having trouble right now. Please try again."
    
    def _is_new_conversation_request(self, user_message):
        """Detect if user is starting a new conversation"""
        new_conversation_indicators = [
            'suggest', 'show', 'list', 'find', 'recommend', 'search',
            'restaurants', 'dining', 'help', 'hello', 'hi',
            'book a table', 'i want to book', 'make a reservation'
        ]
        
        message_lower = user_message.lower()
        
        # If current step is booking_completed and user asks for something new
        if self.booking_context['current_step'] == 'booking_completed':
            if any(indicator in message_lower for indicator in new_conversation_indicators):
                return True
        
        # If asking for restaurants while in middle of different booking
        if any(word in message_lower for word in ['suggest', 'show', 'list', 'find']) and 'restaurant' in message_lower:
            return True
            
        return False
    
    def _update_booking_context_fixed(self, user_message):
        """Fixed context extraction with proper name parsing"""
        message_lower = user_message.lower()
        original_message = user_message  # Keep original for name extraction
        
        # Extract party size
        party_matches = re.findall(r'(\d+)\s*(?:people|person|pax)', message_lower)
        if party_matches:
            self.booking_context['party_size'] = int(party_matches[0])
            print(f"[DEBUG] Extracted party size: {party_matches[0]}")
        
        # Extract date with better parsing
        if 'tomorrow' in message_lower:
            tomorrow = datetime.now() + timedelta(days=1)
            self.booking_context['date'] = tomorrow.strftime("%Y-%m-%d")
            print(f"[DEBUG] Extracted date: tomorrow -> {self.booking_context['date']}")
        elif 'today' in message_lower or 'tonight' in message_lower:
            today = datetime.now()
            self.booking_context['date'] = today.strftime("%Y-%m-%d")
            print(f"[DEBUG] Extracted date: today -> {self.booking_context['date']}")
        
        # Extract time with proper conversion
        time_patterns = [
            r'(\d{1,2}:\d{2})\s*(?:pm|am)',
            r'(\d{1,2})\s*(?:pm|am)'
        ]
        
        for pattern in time_patterns:
            time_matches = re.findall(pattern, message_lower)
            if time_matches:
                time_str = time_matches[0]
                # Convert to 24-hour format
                if 'pm' in message_lower and not time_str.startswith('12'):
                    if ':' in time_str:
                        hour, minute = time_str.split(':')
                        time_str = f"{int(hour) + 12}:{minute}"
                    else:
                        time_str = f"{int(time_str) + 12}:00"
                elif 'am' in message_lower:
                    if not ':' in time_str:
                        time_str = f"{time_str}:00"
                else:
                    if not ':' in time_str:
                        time_str = f"{time_str}:00"
                
                self.booking_context['time'] = time_str
                print(f"[DEBUG] Extracted time: {time_str}")
                break
        
        # Extract restaurant name
        restaurants = get_restaurants_ai()
        for restaurant in restaurants:
            restaurant_name = restaurant['name'].lower()
            if restaurant_name in message_lower:
                self.booking_context['restaurant_name'] = restaurant['name']
                self.booking_context['restaurant_id'] = restaurant['id']
                print(f"[DEBUG] Extracted restaurant: {restaurant['name']} (ID: {restaurant['id']})")
                break
        
        # FIXED: Extract contact info with proper parsing
        self._extract_contact_info_fixed(original_message)
    
    def _extract_contact_info_fixed(self, message):
        """Fixed contact info extraction"""
        message_lower = message.lower()
        
        # FIXED: Better name extraction patterns
        name_patterns = [
            r'my name is ([A-Za-z\s]+?)(?:\s+and|$)',  # Stop at "and" or end
            r'i am ([A-Za-z\s]+?)(?:\s+and|$)',        # Stop at "and" or end
            r'name[:\s]+([A-Za-z\s]+?)(?:\s+and|$)'    # Stop at "and" or end
        ]
        
        for pattern in name_patterns:
            name_matches = re.findall(pattern, message, re.IGNORECASE)
            if name_matches:
                name = name_matches[0].strip()
                # Clean up the name (remove trailing words)
                name_parts = name.split()
                if len(name_parts) > 3:  # If too many words, take first 2-3
                    name = ' '.join(name_parts[:2])
                
                self.booking_context['user_name'] = name
                print(f"[DEBUG] Extracted name: '{name}'")
                break
        
        # FIXED: Better phone extraction
        phone_patterns = [
            r'phone[:\s]*(?:is[:\s]*)?(\d{10,15})',
            r'number[:\s]*(?:is[:\s]*)?(\d{10,15})',
            r'phone[:\s]+(\d{10,15})',
            r'\b(\d{10,15})\b'  # Standalone 10-15 digit number
        ]
        
        for pattern in phone_patterns:
            phone_matches = re.findall(pattern, message)
            if phone_matches:
                phone = phone_matches[0]
                if len(phone) >= 10:
                    self.booking_context['user_phone'] = phone
                    print(f"[DEBUG] Extracted phone: '{phone}'")
                    break
    
    def _classify_intent_enhanced(self, user_message):
        """Enhanced intent classification with recommendation detection"""
        message_lower = user_message.lower()
        context = self.booking_context
        
        # RECOMMENDATION INTENT (NEW)
        recommendation_keywords = [
            'recommend', 'suggest', 'similar', 'like', 'alternatives', 'options',
            'what do you recommend', 'any suggestions', 'help me choose'
        ]
        
        if any(keyword in message_lower for keyword in recommendation_keywords):
            return 'recommendation_request'
        
        # RESTAURANT DISCOVERY INTENT (Enhanced patterns)
        restaurant_discovery_keywords = [
            'show', 'suggest', 'list', 'find', 'recommend', 'search',
            'restaurants', 'dining', 'eat', 'places', 'options'
        ]
        
        # Check if message contains restaurant discovery keywords
        if any(keyword in message_lower for keyword in restaurant_discovery_keywords):
            # Make sure we're not in middle of another booking
            if context['current_step'] in ['initial', 'restaurants_shown', 'booking_completed']:
                return 'show_restaurants'
        
        # BOOKING INTENT
        booking_keywords = ['book', 'reserve', 'reservation', 'table']
        if any(keyword in message_lower for keyword in booking_keywords):
            return 'booking_request'
        
        # RESTAURANT SELECTION
        restaurants = get_restaurants_ai()
        for restaurant in restaurants:
            if restaurant['name'].lower() in message_lower:
                return 'restaurant_selection'
        
        # CONTACT INFO PROVIDED
        if any(pattern in message_lower for pattern in ['name is', 'phone', 'number']):
            return 'contact_info'
        
        # BOOKING DETAILS PROVIDED
        if (re.search(r'\d+\s*(?:people|person)', message_lower) or
            any(word in message_lower for word in ['tomorrow', 'today', 'tonight']) or
            re.search(r'\d+\s*(?:pm|am)', message_lower)):
            return 'booking_details'
        
        # CONFIRMATION
        if any(word in message_lower for word in ['yes', 'yeah', 'ok', 'okay', 'sure', 'proceed']):
            return 'confirmation'
        
        return 'general_conversation'
    
    def _handle_intent(self, intent, user_message):
        """Handle different intents including recommendations"""
        
        if intent == 'recommendation_request':
            return self._handle_recommendation_request(user_message)
        elif intent == 'show_restaurants':
            return self._show_restaurants(user_message)
        elif intent == 'booking_request':
            return self._handle_booking_request(user_message)
        elif intent == 'restaurant_selection':
            return self._handle_restaurant_selection(user_message)
        elif intent == 'contact_info':
            return self._handle_contact_info(user_message)
        elif intent == 'booking_details':
            return self._handle_booking_details(user_message)
        elif intent == 'confirmation':
            return self._handle_confirmation(user_message)
        else:
            return self._handle_general_conversation(user_message)
    
    def _handle_recommendation_request(self, user_message):
        """Handle recommendation requests using the recommendation engine"""
        try:
            print("[DEBUG] Processing recommendation request")
            
            # Get recommendations
            recommendations_data = RecommendationService.get_recommendations_for_user(
                user_message, 
                self.booking_context
            )
            
            # Format for display
            response = RecommendationService.format_recommendations_for_display(recommendations_data)
            
            # Update context with any extracted preferences
            preferences = recommendations_data['user_preferences']
            if preferences.get('cuisine'):
                self.booking_context['cuisine_preference'] = preferences['cuisine']
            if preferences.get('party_size'):
                self.booking_context['party_size'] = preferences['party_size']
            if preferences.get('date'):
                self.booking_context['date'] = preferences['date']
            if preferences.get('time'):
                self.booking_context['time'] = preferences['time']
            
            return response
            
        except Exception as e:
            print(f"[DEBUG] Error handling recommendation request: {e}")
            return "I'd be happy to recommend restaurants! Tell me what type of cuisine you're looking for or any other preferences."
    
    def _show_restaurants(self, user_message):
        """Show restaurants with real-time availability"""
        print("[DEBUG] Executing show_restaurants action")
        
        try:
            # Get fresh restaurant data with real-time availability
            restaurants = get_restaurants_ai()
            print(f"[DEBUG] Retrieved {len(restaurants)} restaurants with real-time availability")
            
            # Enhanced filtering
            cuisine_filter = self._extract_cuisine_preference(user_message)
            location_filter = self._extract_location_preference(user_message)
            
            # Apply filters
            filtered_restaurants = restaurants
            
            if cuisine_filter:
                filtered_restaurants = [r for r in filtered_restaurants 
                                     if cuisine_filter.lower() in r['cuisine'].lower()]
                print(f"[DEBUG] Filtered by cuisine '{cuisine_filter}': {len(filtered_restaurants)} restaurants")
            
            if location_filter:
                filtered_restaurants = [r for r in filtered_restaurants 
                                     if location_filter.lower() in r['location'].lower()]
                print(f"[DEBUG] Filtered by location '{location_filter}': {len(filtered_restaurants)} restaurants")
            
            # If no matches, show all restaurants
            if not filtered_restaurants:
                filtered_restaurants = restaurants[:5]
                filter_text = ""
            else:
                filter_text = f" {cuisine_filter or location_filter}" if (cuisine_filter or location_filter) else ""
            
            # Format response with real-time availability
            response = f"Here are our{filter_text} restaurants:\n\n"
            
            for i, r in enumerate(filtered_restaurants[:5], 1):
                response += f"**{i}. {r['name']}** 🍽️\n"
                response += f"   📍 {r['location']} | 🍜 {r['cuisine']} cuisine\n"
                response += f"   👥 Capacity: {r['capacity']} | ✅ {r['available_tables']} tables available\n\n"
            
            response += "Would you like to book a table at any of these restaurants?"
            
            self.booking_context['current_step'] = 'restaurants_shown'
            return response
            
        except Exception as e:
            print(f"[DEBUG] Error in show_restaurants: {e}")
            return "I'm having trouble loading restaurants right now. Please try again."
    
    def _extract_cuisine_preference(self, message):
        """Extract cuisine preference"""
        message_lower = message.lower()
        cuisines = {
            'italian': ['italian', 'pasta', 'pizza'],
            'indian': ['indian', 'curry', 'spice'],
            'chinese': ['chinese', 'asian', 'wok'],
            'french': ['french', 'bistro'],
            'mexican': ['mexican', 'taco']
        }
        
        for cuisine, keywords in cuisines.items():
            if any(keyword in message_lower for keyword in keywords):
                return cuisine.title()
        return None
    
    def _extract_location_preference(self, message):
        """Extract location preference"""
        message_lower = message.lower()
        locations = ['delhi', 'mumbai', 'downtown', 'midtown', 'uptown', 'chinatown', 'southside']
        
        for location in locations:
            if location in message_lower:
                return location.title()
        return None
    
    def _handle_booking_request(self, user_message):
        """Handle booking requests"""
        context = self.booking_context
        
        missing = []
        if not context.get('restaurant_name'):
            missing.append("restaurant choice")
        if not context.get('party_size'):
            missing.append("party size")
        if not context.get('date'):
            missing.append("date")
        if not context.get('time'):
            missing.append("time")
        
        if missing:
            response = "I'd be happy to help you book a table! "
            response += f"I need: **{', '.join(missing)}**.\n\n"
            response += "💡 **Example:** 'Book a table at Spice Garden for 4 people tomorrow at 7pm'"
            self.booking_context['current_step'] = 'collecting_booking_info'
            return response
        else:
            return self._check_availability_and_proceed()
    
    def _handle_restaurant_selection(self, user_message):
        """Handle restaurant selection"""
        restaurant_name = self.booking_context.get('restaurant_name')
        
        if restaurant_name:
            response = f"Great choice! **{restaurant_name}** it is! "
            
            missing = []
            if not self.booking_context.get('party_size'):
                missing.append("party size")
            if not self.booking_context.get('date'):
                missing.append("date")
            if not self.booking_context.get('time'):
                missing.append("time")
            
            if missing:
                response += f"Now I need: **{', '.join(missing)}**.\n\n"
                response += "💡 **Example:** 'For 4 people tomorrow at 7pm'"
                self.booking_context['current_step'] = 'collecting_booking_details'
            else:
                response += "Let me check availability!"
                response = self._check_availability_and_proceed()
            
            return response
        
        return "Which restaurant would you like to book? Please let me know the name."
    
    def _handle_contact_info(self, user_message):
        """Handle contact information"""
        if self.booking_context.get('user_name') and self.booking_context.get('user_phone'):
            return self._execute_final_booking()
        else:
            missing = []
            if not self.booking_context.get('user_name'):
                missing.append("name")
            if not self.booking_context.get('user_phone'):
                missing.append("phone number")
            
            response = f"I still need your **{' and '.join(missing)}** to complete the booking.\n\n"
            response += "💡 **Example:** 'My name is John Smith and my phone is 9876543210'"
            return response
    
    def _handle_booking_details(self, user_message):
        """Handle booking details"""
        context = self.booking_context
        
        if all([context.get('restaurant_name'), context.get('party_size'), 
                context.get('date'), context.get('time')]):
            return self._check_availability_and_proceed()
        else:
            return self._ask_for_missing_booking_details()
    
    def _handle_confirmation(self, user_message):
        """Handle confirmation"""
        if self.booking_context['current_step'] == 'availability_confirmed':
            return self._ask_for_contact_info()
        elif self.booking_context['current_step'] == 'ready_to_book':
            return self._execute_final_booking()
        else:
            return "What would you like me to help you with?"
    
    def _handle_general_conversation(self, user_message):
        """Handle general conversation"""
        return "I can help you find restaurants and make reservations. Try asking me to 'show restaurants' or 'book a table'!"
    
    def _check_availability_and_proceed(self):
        """Check availability with real-time updates"""
        context = self.booking_context
        
        try:
            print(f"[DEBUG] Checking real-time availability for restaurant {context['restaurant_id']}")
            
            availability_result = check_availability_ai(
                restaurant_id=context['restaurant_id'],
                party_size=context['party_size'],
                date=context['date'],
                time=context['time']
            )
            
            print(f"[DEBUG] Real-time availability result: {availability_result}")
            
            if availability_result.get('available'):
                context['table_id'] = availability_result.get('suggested_table_id')
                context['current_step'] = 'availability_confirmed'
                
                response = f"✅ **Great!** Table available at **{context['restaurant_name']}**:\n\n"
                response += f"👥 **{context['party_size']} people** on **{context['date']}** at **{context['time']}**\n\n"
                
                if not context.get('user_name') or not context.get('user_phone'):
                    response += "To complete booking, I need your contact details:\n"
                    response += "💡 **Example:** 'My name is John Smith and phone is 9876543210'"
                    return response
                else:
                    return self._execute_final_booking()
            else:
                error_msg = availability_result.get('error', 'No tables available')
                return f"❌ Sorry, no tables available at **{context['restaurant_name']}** for your requested time.\n\nError: {error_msg}\n\nTry a different time or restaurant?"
                
        except Exception as e:
            print(f"[DEBUG] Error checking availability: {e}")
            return f"❌ Error checking availability: {str(e)}"
    
    def _ask_for_missing_booking_details(self):
        """Ask for missing details"""
        context = self.booking_context
        
        missing = []
        if not context.get('restaurant_name'):
            missing.append("restaurant")
        if not context.get('party_size'):
            missing.append("party size")
        if not context.get('date'):
            missing.append("date")
        if not context.get('time'):
            missing.append("time")
        
        response = f"I need: **{', '.join(missing)}** to check availability.\n\n"
        response += "💡 **Example:** 'For 4 people at Spice Garden tomorrow at 7pm'"
        return response
    
    def _ask_for_contact_info(self):
        """Ask for contact info"""
        response = "Perfect! Now I need your contact information:\n\n"
        response += "• **Your name**\n"
        response += "• **Phone number**\n\n"
        response += "💡 **Example:** 'My name is John Smith and my phone is 9876543210'"
        self.booking_context['current_step'] = 'collecting_contact'
        return response
    
    def _execute_final_booking(self):
        """Execute final booking with real-time availability update"""
        context = self.booking_context
        
        try:
            print(f"[DEBUG] Making final reservation with real-time update: {context}")
            
            reservation_result = make_reservation_ai(
                user_name=context['user_name'],
                user_phone=context['user_phone'],
                restaurant_id=context['restaurant_id'],
                table_id=context.get('table_id', 1),
                party_size=context['party_size'],
                date=context['date'],
                time=context['time'],
                user_email=""
            )
            
            print(f"[DEBUG] Reservation result with availability update: {reservation_result}")
            
            if reservation_result.get('success'):
                reservation_id = reservation_result.get('reservation_id', 'N/A')
                context['current_step'] = 'booking_completed'
                
                response = f"🎉 **Reservation Confirmed!**\n\n"
                response += f"**📋 Details:**\n"
                response += f"• **Reservation ID:** `{reservation_id}`\n"
                response += f"• **Restaurant:** {context['restaurant_name']}\n"
                response += f"• **Name:** {context['user_name']}\n"
                response += f"• **Phone:** {context['user_phone']}\n"
                response += f"• **Party:** {context['party_size']} people\n"
                response += f"• **Date:** {context['date']}\n"
                response += f"• **Time:** {context['time']}\n\n"
                response += f"📱 **Please arrive 10 minutes early!**\n\n"
                response += f"*Table availability has been updated in real-time.*"
                
                return response
            else:
                error_msg = reservation_result.get('error', 'Unknown error')
                return f"❌ Booking failed: {error_msg}"
                
        except Exception as e:
            print(f"[DEBUG] Error making reservation: {e}")
            return f"❌ Error making reservation: {str(e)}"
    
    def reset_conversation(self):
        """Reset conversation properly"""
        print("[DEBUG] Resetting conversation and context")
        self.conversation = []
        self.booking_context = {
            'restaurant_name': None,
            'restaurant_id': None,
            'party_size': None,
            'date': None,
            'time': None,
            'user_name': None,
            'user_phone': None,
            'current_step': 'initial'
        }
    
    def get_booking_status(self):
        """Get booking status"""
        return {
            "booking_context": self.booking_context,
            "current_step": self.booking_context.get('current_step'),
            "ready_to_book": all([
                self.booking_context.get('restaurant_name'),
                self.booking_context.get('party_size'),
                self.booking_context.get('date'),
                self.booking_context.get('time'),
                self.booking_context.get('user_name'),
                self.booking_context.get('user_phone')
            ])
        }