import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import json
from typing import List, Dict, Tuple
from restaurant.database import session
from restaurant.models import Restaurant, Table

class RestaurantRecommendationEngine:
    """Intelligent restaurant recommendation system with cuisine matching and availability optimization"""
    
    def __init__(self):
        print("[DEBUG] Initializing Restaurant Recommendation Engine...")
        self.restaurants_df = None
        self.cuisine_similarity_matrix = None
        self.tfidf_vectorizer = None
        self.load_restaurant_data()
        self.build_recommendation_models()
        print("[DEBUG] ✅ Recommendation Engine ready")
    
    def load_restaurant_data(self):
        """Load restaurant data into pandas DataFrame for analysis"""
        try:
            restaurants = session.query(Restaurant).all()
            
            # Convert to DataFrame for analysis
            data = []
            for restaurant in restaurants:
                # Count available tables
                available_tables = session.query(Table).filter_by(
                    restaurant_id=restaurant.id,
                    is_available=True
                ).count()
                
                data.append({
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'cuisine': restaurant.cuisine,
                    'location': restaurant.location,
                    'capacity': restaurant.capacity,
                    'available_tables': available_tables,
                    'cuisine_keywords': self._extract_cuisine_keywords(restaurant.cuisine),
                    'location_keywords': self._extract_location_keywords(restaurant.location)
                })
            
            self.restaurants_df = pd.DataFrame(data)
            print(f"[DEBUG] Loaded {len(self.restaurants_df)} restaurants into recommendation engine")
            
        except Exception as e:
            print(f"[DEBUG] Error loading restaurant data: {e}")
            self.restaurants_df = pd.DataFrame()
    
    def _extract_cuisine_keywords(self, cuisine: str) -> str:
        """Extract and expand cuisine keywords for better matching"""
        cuisine_expansions = {
            'italian': 'italian pasta pizza mediterranean european',
            'indian': 'indian curry spicy asian tandoori',
            'chinese': 'chinese asian wok stir-fry noodles',
            'french': 'french european fine-dining bistro',
            'mexican': 'mexican latin spicy tex-mex',
            'american': 'american comfort casual burgers',
            'japanese': 'japanese asian sushi ramen',
            'seafood': 'seafood fish ocean coastal',
            'steakhouse': 'steakhouse meat grill american'
        }
        
        cuisine_lower = cuisine.lower()
        for key, expansion in cuisine_expansions.items():
            if key in cuisine_lower:
                return expansion
        
        return cuisine_lower
    
    def _extract_location_keywords(self, location: str) -> str:
        """Extract location-based keywords"""
        location_keywords = {
            'downtown': 'downtown central business urban',
            'midtown': 'midtown central business',
            'uptown': 'uptown residential quiet',
            'chinatown': 'chinatown ethnic cultural',
            'little italy': 'little-italy ethnic cultural',
            'financial': 'financial business corporate',
            'village': 'village trendy artistic'
        }
        
        location_lower = location.lower()
        for key, keywords in location_keywords.items():
            if key in location_lower:
                return keywords
        
        return location_lower
    
    def build_recommendation_models(self):
        """Build recommendation models using TF-IDF and cosine similarity"""
        if self.restaurants_df.empty:
            print("[DEBUG] No restaurant data available for building models")
            return
        
        try:
            # Combine cuisine and location features
            self.restaurants_df['combined_features'] = (
                self.restaurants_df['cuisine_keywords'] + ' ' + 
                self.restaurants_df['location_keywords']
            )
            
            # Build TF-IDF matrix
            self.tfidf_vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=100
            )
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(
                self.restaurants_df['combined_features']
            )
            
            # Calculate cosine similarity matrix
            self.cuisine_similarity_matrix = cosine_similarity(tfidf_matrix)
            
            print("[DEBUG] ✅ Built recommendation models using TF-IDF and cosine similarity")
            
        except Exception as e:
            print(f"[DEBUG] Error building recommendation models: {e}")
    
    def get_cuisine_based_recommendations(self, target_restaurant_id: int, num_recommendations: int = 5) -> List[Dict]:
        """Get restaurant recommendations based on cuisine similarity"""
        try:
            if self.cuisine_similarity_matrix is None:
                return []
            
            # Find target restaurant index
            target_idx = self.restaurants_df[
                self.restaurants_df['id'] == target_restaurant_id
            ].index[0]
            
            # Get similarity scores
            similarity_scores = list(enumerate(self.cuisine_similarity_matrix[target_idx]))
            
            # Sort by similarity (excluding self)
            similarity_scores = [
                (idx, score) for idx, score in similarity_scores 
                if idx != target_idx
            ]
            similarity_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get top recommendations
            recommendations = []
            for idx, score in similarity_scores[:num_recommendations]:
                restaurant_data = self.restaurants_df.iloc[idx]
                recommendations.append({
                    'restaurant_id': int(restaurant_data['id']),
                    'name': restaurant_data['name'],
                    'cuisine': restaurant_data['cuisine'],
                    'location': restaurant_data['location'],
                    'similarity_score': float(score),
                    'available_tables': int(restaurant_data['available_tables']),
                    'recommendation_reason': f"Similar {restaurant_data['cuisine']} cuisine"
                })
            
            print(f"[DEBUG] Generated {len(recommendations)} cuisine-based recommendations")
            return recommendations
            
        except Exception as e:
            print(f"[DEBUG] Error generating cuisine recommendations: {e}")
            return []
    
    def get_alternative_time_slots(self, restaurant_id: int, preferred_date: str, preferred_time: str, party_size: int) -> List[Dict]:
        """Suggest alternative time slots when preferred time is not available"""
        try:
            from ai.services import check_availability_ai
            
            # Parse preferred time
            preferred_datetime = datetime.strptime(f"{preferred_date} {preferred_time}", "%Y-%m-%d %H:%M")
            
            # Generate alternative time slots (±2 hours in 30-minute intervals)
            alternative_slots = []
            
            for offset_minutes in [-120, -90, -60, -30, 30, 60, 90, 120]:
                alt_datetime = preferred_datetime + timedelta(minutes=offset_minutes)
                alt_time = alt_datetime.strftime("%H:%M")
                alt_date = alt_datetime.strftime("%Y-%m-%d")
                
                # Skip if too early or too late
                if alt_datetime.hour < 17 or alt_datetime.hour > 22:
                    continue
                
                # Check availability
                availability = check_availability_ai(restaurant_id, party_size, alt_date, alt_time)
                
                if availability.get('available'):
                    alternative_slots.append({
                        'date': alt_date,
                        'time': alt_time,
                        'datetime_str': alt_datetime.strftime("%Y-%m-%d %H:%M"),
                        'display_time': alt_datetime.strftime("%I:%M %p"),
                        'display_date': alt_datetime.strftime("%A, %B %d"),
                        'offset_minutes': offset_minutes,
                        'table_id': availability.get('suggested_table_id')
                    })
            
            # Sort by closeness to preferred time
            alternative_slots.sort(key=lambda x: abs(x['offset_minutes']))
            
            print(f"[DEBUG] Found {len(alternative_slots)} alternative time slots")
            return alternative_slots[:5]  # Return top 5 alternatives
            
        except Exception as e:
            print(f"[DEBUG] Error generating alternative time slots: {e}")
            return []
    
    def get_availability_based_recommendations(self, party_size: int, date: str, time: str, cuisine_preference: str = None) -> List[Dict]:
        """Recommend restaurants based on availability and preferences"""
        try:
            from ai.services import check_availability_ai
            
            available_restaurants = []
            
            for _, restaurant in self.restaurants_df.iterrows():
                # Check availability
                availability = check_availability_ai(
                    int(restaurant['id']), party_size, date, time
                )
                
                if availability.get('available'):
                    # Calculate recommendation score
                    score = self._calculate_availability_score(
                        restaurant, cuisine_preference, availability
                    )
                    
                    available_restaurants.append({
                        'restaurant_id': int(restaurant['id']),
                        'name': restaurant['name'],
                        'cuisine': restaurant['cuisine'],
                        'location': restaurant['location'],
                        'capacity': int(restaurant['capacity']),
                        'available_tables': int(restaurant['available_tables']),
                        'recommendation_score': score,
                        'table_id': availability.get('suggested_table_id'),
                        'recommendation_reason': self._get_recommendation_reason(restaurant, cuisine_preference)
                    })
            
            # Sort by recommendation score
            available_restaurants.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            print(f"[DEBUG] Found {len(available_restaurants)} available restaurants")
            return available_restaurants
            
        except Exception as e:
            print(f"[DEBUG] Error generating availability-based recommendations: {e}")
            return []
    
    def _calculate_availability_score(self, restaurant: pd.Series, cuisine_preference: str, availability: Dict) -> float:
        """Calculate recommendation score based on multiple factors"""
        score = 0.0
        
        # Base score for availability
        score += 10.0
        
        # Cuisine preference bonus
        if cuisine_preference and cuisine_preference.lower() in restaurant['cuisine'].lower():
            score += 20.0
        
        # Capacity utilization bonus (prefer restaurants with good but not full capacity)
        utilization = (restaurant['capacity'] - restaurant['available_tables']) / restaurant['capacity']
        if 0.3 <= utilization <= 0.7:  # Sweet spot for atmosphere
            score += 10.0
        
        # Popular location bonus
        popular_locations = ['downtown', 'midtown', 'village']
        if any(loc in restaurant['location'].lower() for loc in popular_locations):
            score += 5.0
        
        return score
    
    def _get_recommendation_reason(self, restaurant: pd.Series, cuisine_preference: str) -> str:
        """Generate human-readable recommendation reason"""
        reasons = []
        
        if cuisine_preference and cuisine_preference.lower() in restaurant['cuisine'].lower():
            reasons.append(f"Matches your {cuisine_preference} preference")
        
        if restaurant['available_tables'] > 5:
            reasons.append("Good availability")
        
        popular_locations = ['downtown', 'midtown', 'village']
        if any(loc in restaurant['location'].lower() for loc in popular_locations):
            reasons.append("Popular location")
        
        if not reasons:
            reasons.append("Available now")
        
        return " • ".join(reasons)
    
    def get_smart_recommendations(self, user_preferences: Dict) -> Dict:
        """Get comprehensive smart recommendations based on user preferences"""
        try:
            print(f"[DEBUG] Generating smart recommendations for: {user_preferences}")
            
            party_size = user_preferences.get('party_size', 2)
            date = user_preferences.get('date')
            time = user_preferences.get('time')
            cuisine_preference = user_preferences.get('cuisine')
            location_preference = user_preferences.get('location')
            
            recommendations = {
                'primary_recommendations': [],
                'alternative_times': [],
                'similar_cuisines': [],
                'popular_choices': []
            }
            
            # Primary recommendations based on availability
            if date and time:
                recommendations['primary_recommendations'] = self.get_availability_based_recommendations(
                    party_size, date, time, cuisine_preference
                )[:5]
            
            # Alternative time slots if primary has few options
            if date and time and len(recommendations['primary_recommendations']) < 3:
                # Use the first available restaurant for alternative times
                first_restaurant_id = self.restaurants_df.iloc[0]['id']
                recommendations['alternative_times'] = self.get_alternative_time_slots(
                    int(first_restaurant_id), date, time, party_size
                )
            
            # Similar cuisine recommendations
            if cuisine_preference:
                cuisine_restaurants = self.restaurants_df[
                    self.restaurants_df['cuisine'].str.contains(cuisine_preference, case=False, na=False)
                ]
                if not cuisine_restaurants.empty:
                    target_restaurant_id = int(cuisine_restaurants.iloc[0]['id'])
                    recommendations['similar_cuisines'] = self.get_cuisine_based_recommendations(
                        target_restaurant_id, 5
                    )
            
            # Popular choices (high capacity, good availability)
            popular_restaurants = self.restaurants_df[
                (self.restaurants_df['capacity'] >= 80) & 
                (self.restaurants_df['available_tables'] >= 5)
            ].head(5)
            
            recommendations['popular_choices'] = [
                {
                    'restaurant_id': int(row['id']),
                    'name': row['name'],
                    'cuisine': row['cuisine'],
                    'location': row['location'],
                    'capacity': int(row['capacity']),
                    'available_tables': int(row['available_tables']),
                    'recommendation_reason': 'Popular choice with good availability'
                }
                for _, row in popular_restaurants.iterrows()
            ]
            
            print(f"[DEBUG] Generated comprehensive recommendations")
            return recommendations
            
        except Exception as e:
            print(f"[DEBUG] Error generating smart recommendations: {e}")
            return {
                'primary_recommendations': [],
                'alternative_times': [],
                'similar_cuisines': [],
                'popular_choices': []
            }

# Global recommendation engine instance
recommendation_engine = RestaurantRecommendationEngine()
