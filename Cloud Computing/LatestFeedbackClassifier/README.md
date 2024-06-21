# Project Description

This project is a Flask-based web application that provides an API to predict whether each of latest reviews of a place id is critique or recommendation or neither.

## Table of Contents

- [Introduction](#introduction)
- [File Structure](#file-structure)
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)
- [License](#license)

## Introduction

This repository contains a Flask application designed to retrieve data with given place id from Google Maps API and then get the latest reviews. The latest reviews then get filtered to select only reviews with minimum characters length of 50. After that, the reviews will get predicted by the FeedbackClassifier.h5 model and give output of prediction.

## File Structure

method/ <br>
├── predicting.py # Module for predicting whether the review is of critique or recommendation or neither <br>
├── preparing.py # Module for preparing dataset before prediction phase <br>
├── preprocessing.py # Module for preprocessing <br>
Model/ <br>
├── FeedbackClassifier.h5 # Critique or Recommendation or Neither Classification Model <br>
app.py # Flask application main file <br>
demo.py # For demonstration purpose
requirements.txt # File listing dependencies <br>

## Endpoints

- `/predict` (POST) : Accepts JSON data containing latitude and longitude, performs dynamic clustering using TensorFlow, and returns the clustered results.

## Dependencies

- Flask (3.0.\*)
- functions-framework (3.\*)
- google-cloud-bigquery (3.23.0)
- google-cloud-storage (2.17.0)
- pandas (2.2.\*)
- scikit-learn (1.5.\*)
- gunicorn

## License

MIT License
