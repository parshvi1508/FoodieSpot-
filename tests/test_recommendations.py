"""Test recommendation system"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.recommendation_service import RecommendationService
from ai.recommendation_engine import recommendation_engine

def test_cuisine_recommendations():
    """Test cuisine-based recommendations"""
    print("🧪 Testing Cuisine Recommendations")
    print("-" * 40)
    
    try:
        # Test with first restaurant
        if not recommendation_engine.restaurants_df.empty:
            first_restaurant_id = int(recommendation_engine.restaurants_df.iloc[0]['id'])
            recommendations = recommendation_engine.get_cuisine_based_recommendations(first_restaurant_id, 3)
            
            print(f"✅ Found {len(recommendations)} similar restaurants")
            for rec in recommendations:
                print(f"  • {rec['name']} ({rec['cuisine']}) - Score: {rec['similarity_score']:.3f}")
        else:
            print("❌ No restaurant data available")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_time_alternatives():
    """Test alternative time suggestions"""
    print("\n🧪 Testing Alternative Time Slots")
    print("-" * 40)
    
    try:
        if not recommendation_engine.restaurants_df.empty:
            first_restaurant_id = int(recommendation_engine.restaurants_df.iloc[0]['id'])
            alternatives = recommendation_engine.get_alternative_time_slots(
                first_restaurant_id, "2025-05-28", "19:00", 4
            )
            
            print(f"✅ Found {len(alternatives)} alternative time slots")
            for alt in alternatives:
                print(f"  • {alt['display_date']} at {alt['display_time']}")
        else:
            print("❌ No restaurant data available")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_smart_recommendations():
    """Test comprehensive smart recommendations"""
    print("\n🧪 Testing Smart Recommendations")
    print("-" * 40)
    
    try:
        preferences = {
            'party_size': 4,
            'date': '2025-05-28',
            'time': '19:00',
            'cuisine': 'Italian'
        }
        
        recommendations = recommendation_engine.get_smart_recommendations(preferences)
        
        print(f"✅ Primary recommendations: {len(recommendations['primary_recommendations'])}")
        print(f"✅ Alternative times: {len(recommendations['alternative_times'])}")
        print(f"✅ Similar cuisines: {len(recommendations['similar_cuisines'])}")
        print(f"✅ Popular choices: {len(recommendations['popular_choices'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_recommendation_service():
    """Test recommendation service integration"""
    print("\n🧪 Testing Recommendation Service")
    print("-" * 40)
    
    try:
        user_inputs = [
            "Recommend Italian restaurants for 4 people tomorrow at 7pm",
            "Suggest similar restaurants",
            "What alternatives do you have?",
            "Show me Chinese restaurants"
        ]
        
        for user_input in user_inputs:
            print(f"\nUser: {user_input}")
            recommendations_data = RecommendationService.get_recommendations_for_user(user_input)
            response = RecommendationService.format_recommendations_for_display(recommendations_data)
            print(f"Response: {response[:200]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 Testing Issue 5: Recommendation System")
    print("=" * 50)
    
    test_cuisine_recommendations()
    test_time_alternatives()
    test_smart_recommendations()
    test_recommendation_service()
    
    print("\n✅ Recommendation system testing complete!")
