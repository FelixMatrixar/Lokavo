from flask import Flask, request, jsonify

import json
import pandas as pd
import tensorflow as tf
import tensorflow_text as text
import nltk

from method.predicting import *
from method.preparing import *
from method.preprocessing import *

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        request_json = request.get_json()
        argplace_id = request_json.get("argplace_id")
        
        # Get the reviews
        reviews = get_new_data(argplace_id)
        if reviews is None:
            return None
        
        # Process each review
        processed_reviews = [review_to_words(review) for review in reviews]
        
        # Predict each processed review
        predictions = [predict_review(review, CLASSIFIER) for review in processed_reviews]

        # Translate predictions to labels
        translated_predictions = [
            "Critique or Recommendation Feedback" if pred == 1 else "Not"
            for pred in predictions
        ]
    
        return translated_predictions
    
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500  # Return error message with status code 500 (Internal Server Error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
