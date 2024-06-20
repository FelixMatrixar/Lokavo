# Project Description

This Flask-based application interacts with Google Cloud services to analyze competitor reviews and provide insights via lightweight stay-in-context chatbot.

## Table of Contents

- [Introduction](#introduction)
- [File Structure](#file-structure)
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)
- [License](#license)

## Introduction

This project is a Flask application that uses Google Cloud services (Google Cloud Storage) to manage and analyze competitor reviews. It provides functionalities to extract reviews based on geographical coordinates, translate them, summarize them, and upload the results back to Google Cloud Storage.

## File Structure

demo/ <br>
├── chatbot.json # JSON file for demonstration purposes <br>
├── chatbot.py # Main application file <br>
method/ <br>
├── nearbycompetitors.py # Module for handling nearby competitors <br>
├── queries.py # Module for database queries (if applicable) <br>
└── responses.py # Module for handling API responses <br>
app.py # Flask application main file <br>
requirements.txt # File listing dependencies <br>

- `demo/`: Contains a demo JSON file (`chatbot.json`) showcasing application output.
- `method/`: Directory for various Python modules handling application logic.
- `app.py`: Main Flask application file.
- `requirements.txt`: List of Python packages required to run the application.

## Endpoints

- `/chatbot` (POST): Accepts JSON data with latitude, longitude, and UUID to fetch competitor reviews, generate markdown files, and upload them to Google Cloud Storage.
- `/chatbot/<uuid>/<type>` (GET): Retrieves the processed markdown file from Google Cloud Storage based on UUID and type.

## Dependencies

- Flask (3.0.\*)
- functions-framework (3.\*)
- google-cloud-bigquery (3.23.0)
- google-cloud-storage (2.17.0)
- pandas (2.2.\*)
- gunicorn

## License

MIT License
