from typing import Dict, List
from .recommendation_engine import recommendation_engine
from datetime import datetime, timedelta

class RecommendationService:
    """Service layer for restaurant recommendations"""
    
    @staticmethod
    def get_recommendations_for_user(user_input: str, context: Dict = None) -> Dict:
        """Get recommendations based on user input and context"""
        print(f"[DEBUG] Getting recommendations for user input: {user_input}")
        
        # Extract preferences from user input
        preferences = RecommendationService._extract_preferences(user_input, context)
        
        # Get smart recommendations
        recommendations = recommendation_engine.get_smart_recommendations(preferences)
        
        return {
            'user_preferences': preferences,
            'recommendations': recommendations,
            'recommendation_type': RecommendationService._determine_recommendation_type(preferences)
        }
    
    @staticmethod
    def _extract_preferences(user_input: str, context: Dict = None) -> Dict:
        """Extract user preferences from input"""
        preferences = {}
        user_lower = user_input.lower()
        
        # Extract cuisine preference
        cuisines = ['italian', 'indian', 'chinese', 'french', 'mexican', 'american', 'japanese']
        for cuisine in cuisines:
            if cuisine in user_lower:
                preferences['cuisine'] = cuisine.title()
                break
        
        # Extract party size
        import re
        party_match = re.search(r'(\d+)\s*(?:people|person)', user_lower)
        if party_match:
            preferences['party_size'] = int(party_match.group(1))
        elif context and context.get('party_size'):
            preferences['party_size'] = context['party_size']
        
        # Extract date preference
        if 'tomorrow' in user_lower:
            tomorrow = datetime.now() + timedelta(days=1)
            preferences['date'] = tomorrow.strftime('%Y-%m-%d')
        elif 'today' in user_lower or 'tonight' in user_lower:
            preferences['date'] = datetime.now().strftime('%Y-%m-%d')
        elif context and context.get('date'):
            preferences['date'] = context['date']
        
        # Extract time preference
        time_match = re.search(r'(\d{1,2})\s*(?:pm|am)', user_lower)
        if time_match:
            hour = int(time_match.group(1))
            if 'pm' in user_lower and hour != 12:
                hour += 12
            preferences['time'] = f"{hour:02d}:00"
        elif context and context.get('time'):
            preferences['time'] = context['time']
        
        # Extract location preference
        locations = ['downtown', 'midtown', 'uptown', 'village']
        for location in locations:
            if location in user_lower:
                preferences['location'] = location.title()
                break
        
        return preferences
    
    @staticmethod
    def _determine_recommendation_type(preferences: Dict) -> str:
        """Determine the type of recommendation needed"""
        if preferences.get('date') and preferences.get('time'):
            return 'availability_based'
        elif preferences.get('cuisine'):
            return 'cuisine_based'
        else:
            return 'general'
    
    @staticmethod
    def format_recommendations_for_display(recommendations_data: Dict) -> str:
        """Format recommendations for display in chat"""
        try:
            preferences = recommendations_data['user_preferences']
            recommendations = recommendations_data['recommendations']
            
            response = "🎯 **Here are my recommendations for you:**\n\n"
            
            # Show user preferences
            if preferences:
                response += "**Based on your preferences:**\n"
                if preferences.get('cuisine'):
                    response += f"• Cuisine: {preferences['cuisine']}\n"
                if preferences.get('party_size'):
                    response += f"• Party size: {preferences['party_size']} people\n"
                if preferences.get('date'):
                    response += f"• Date: {preferences['date']}\n"
                if preferences.get('time'):
                    response += f"• Time: {preferences['time']}\n"
                response += "\n"
            
            # Primary recommendations
            if recommendations['primary_recommendations']:
                response += "**🍽️ Best Matches:**\n"
                for i, rec in enumerate(recommendations['primary_recommendations'][:3], 1):
                    response += f"{i}. **{rec['name']}** ({rec['cuisine']})\n"
                    response += f"   📍 {rec['location']} • {rec['recommendation_reason']}\n\n"
            
            # Alternative times
            if recommendations['alternative_times']:
                response += "**⏰ Alternative Times:**\n"
                for alt in recommendations['alternative_times'][:3]:
                    response += f"• {alt['display_date']} at {alt['display_time']}\n"
                response += "\n"
            
            # Similar cuisines
            if recommendations['similar_cuisines']:
                response += "**🍜 Similar Restaurants:**\n"
                for rec in recommendations['similar_cuisines'][:3]:
                    response += f"• **{rec['name']}** ({rec['cuisine']}) - {rec['location']}\n"
                response += "\n"
            
            # Popular choices
            if recommendations['popular_choices'] and not recommendations['primary_recommendations']:
                response += "**⭐ Popular Choices:**\n"
                for rec in recommendations['popular_choices'][:3]:
                    response += f"• **{rec['name']}** ({rec['cuisine']}) - {rec['location']}\n"
                response += "\n"
            
            response += "Would you like to book any of these restaurants? Just let me know which one!"
            
            return response
            
        except Exception as e:
            print(f"[DEBUG] Error formatting recommendations: {e}")
            return "I found some great recommendations for you! Let me know what type of cuisine you're interested in."

# Export for use in agent
__all__ = ['RecommendationService']
