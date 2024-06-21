import tensorflow as tf
import tensorflow_hub as hub

CLASSIFIER =  tf.keras.models.load_model('Model/FeedbackClassifier.h5', custom_objects={'KerasLayer': hub.KerasLayer})

# Function to predict a single review and return 0 or 1
def predict_review(preprocessed_review, classifier_model):
    
    probability = classifier_model.predict([preprocessed_review])[0][0]

    # Return 1 if the probability is greater than or equal to 0.5, else return 0
    return 1 if probability >= 0.5 else 0
    
