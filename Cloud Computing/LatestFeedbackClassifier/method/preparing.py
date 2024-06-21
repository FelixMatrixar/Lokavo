import requests

from secret_config import *

# Get New Data from Google Maps API
def get_new_data(place_id, api_key=API_KEY):
    # Endpoint to get details about a place
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    # Parameters
    params = {
        'place_id': place_id,
        'fields': 'review',
        'key': api_key
    }
    
    # Sending request
    response = requests.get(endpoint_url, params=params)
    
    # Parsing the response
    if response.status_code == 200:
        data = response.json()

        # Extract reviews and filter based on text length > 50
        filtered_reviews = [
            review['text'] for review in data['result'].get('reviews', [])
            if len(review.get('text', '')) > 50
        ]
        
        return filtered_reviews
    else:
        return None