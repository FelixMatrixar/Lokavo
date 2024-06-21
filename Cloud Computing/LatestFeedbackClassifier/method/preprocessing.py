from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import nltk
import re

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def review_to_words(raw_review):
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review, 'lxml').get_text() 
    print("After removing HTML:", review_text)
    
    # 2. Tokenize words
    words = word_tokenize(review_text)
    print("After tokenization:", words)
    
    # 3. Convert to lower case
    words = [word.lower() for word in words]
    print("After lowercasing:", words)
    
    # 4. Remove non-alphabetic characters and numbers
    words = [re.sub("[^a-zA-Z]", "", word) for word in words]
    print("After removing non-alphabetic characters:", words)
    
    # 5. Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    print("After lemmatization:", words)
    
    # 6. Create set of stopwords
    stops = set(stopwords.words("english"))
    
    # 7. Remove stop words
    meaningful_words = [word for word in words if word not in stops]
    print("After removing stopwords:", meaningful_words)
    
    # 8. Join the words back into one string separated by space
    processed_review = " ".join(meaningful_words)
    print("Final processed review:", processed_review)
    
    return processed_review
