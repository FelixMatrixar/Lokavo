# Project Description

This project aims to support F&B businesses by providing valuable insights into their competitive landscape with machine learning approach. It utilizes data scraping techniques to gather comprehensive information from Google Maps about various F&B establishments. By leveraging advanced data analysis methods, this project enhances decision-making capabilities for businesses seeking to optimize their strategies and stay competitive in the market.

## Table of Contents

- [Introduction](#introduction)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [License](#license)

## Introduction

This repository contains Lokavo: Local Ventures' machine learning components, focusing on crucial technical implementations for optimizing F&B businesses. It includes scraping and preprocessing data from Google Maps to create detailed profiles of F&B venues in Java Island. The repository utilizes TensorFlow to cluster customer data and identify different segments. Additionally, it incorporates BERT models for sentiment analysis to effectively classify customer reviews, distinguishing between critiques/suggestions or not. These capabilities provide businesses with insights into customer preferences, operational trends, and competitive positioning, helping them make data-driven decisions and refine their strategies.

## File Structure

File Scraping/ <br>
├── Banten # Folder containing scraping files from Banten province <br>
├── DIY # Folder containing scraping files from Daerah Istimewa Yogyakarta province <br>
├── DKI Jakarta # Folder containing scraping files from Jakarta province <br>
├── Full Jakarta # Folder containing completed scraping files from Jakarta province <br>
├── Jawa Barat # Folder containing scraping files from Jawa Barat province <br>
├── Jawa Tengah # Folder containing scraping files from Jawa Tengah province <br>
└── Jawa Timur # Folder containing scraping files from Jawa Timur province <br>
kritik dataset/ <br>
├── df_neg_[number].csv # Data containing 5000 negatively sentimented reviews that have been labeled <br>
└── df_pos_[number].csv # Data containing 5000 positively sentimented reviews that have been labeled <br>
Sentiment Analysis/ <br>
├── CompleteReviews.csv # Data containing full reviews that have been labeled <br>
├── criticism_dataset.csv # Data containing labeled reviews that have been preprocessed <br>
├── english_review.csv # Data containing English reviews <br>
├── FeedbackClassifier.h5 # Model of sentiment analysis <br>
├── Prediction.ipynb # Notebook containing the prediction process for review data <br>
├── TextModelling.ipynb # Notebook containing the modeling process for review data <br>
├── train_validation.csv # Data containing training set and validation set for modeling <br>
└── train_validation_test.csv # Data containing training set, validation set, and test set for modeling <br>
Preprocessing.ipynb # Notebook containing preprocessing for data scraping <br>
category_groups.txt # JSON file containing groupings of different types of places and services  <br>
Clustering_Model.ipynb # Notebook containing functions for clustering or competitor segmentation process <br>
full_data.csv # Data containing preprocessed place details <br>
Review_Preprocessing.ipynb # Notebook containing preprocessing of review data <br>

- `File Scraping/`: Directory for containing scraping results from 6 provinces on the island of Java with the complete province of DKI Jakarta.
- `kritik dataset/`: Directory for containing 10,000 lines of reviews taken randomly and labeled whether the review contains criticism/suggestions or not.
- `Sentiment Analysis/`: Directory for containing the process of creating a sentiment analysis model along with its predictions.

## Dependencies

- Numpy
- Pandas
- Matplotlib
- Seaborn
- TensorFlow
- Scikit-learn
- Scipy
- TensorFlow Hub
- TensorFlow Text
- NLTK
- BeautifulSoup4

## License

MIT License
