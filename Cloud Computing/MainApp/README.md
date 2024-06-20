# Project Description

This project is a Flask-based web application that provides a set of APIs to assist businesses in understanding their competitive landscape. The application leverages BigQuery to fetch details about nearby competitors and uses custom services (deployed other Cloud Run) to model and analyze competitor data. Additionally, the application offers endpoints to retrieve top competitors, relevant business articles, helping users stay informed about industry trends and insights.

## Table of Contents

- [Introduction](#introduction)
- [File Structure](#file-structure)
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)
- [License](#license)

## Introduction

This repository contains a Flask application designed to retrieve data about nearby competitors, initiate clustering processes on another cloud run service, identify top competitors, and fetch relevant business articles. The primary purpose of separating this repository from the DynamicClustering repository is to reduce the development time associated with building large Docker image files. By offloading intensive clustering operations to a separate cloud run service, the application maintains optimal performance and faster development cycles. This modular approach not only enhances maintainability but also reduces the complexity associated with large Docker images, making the development process more efficient.

## File Structure

demo/ <br>
├── competitor_details.json # JSON file for competitor details <br>
├── competitor_details.py # Script for competitor details <br>
├── modelling_results.json # JSON file for modelling results <br>
├── modelling_results.py # Script for modelling results <br>
├── top_competitors.json # JSON file for top competitors <br>
└── top_competitors.py # Script for top competitors <br>
method/ <br>
├── articles.py # Module for handling articles <br>
├── inferencing.py # Module for inferencing <br>
├── modelling.py # Module for modelling <br>
├── nearbycompetitors.py # Module for handling nearby competitors <br>
├── preprocessing.py # Module for preprocessing data <br>
├── queries.py # Module for database queries <br>
├── responses.py # Module for handling API responses <br>
└── visualizing.py # Module for visualizing data <br>
app.py # Flask application main file <br>
requirements.txt # File listing dependencies <br>

## Endpoints

- `/modelling_results` (POST) : Accepts JSON data containing latitude and longitude, performs dynamic clustering using TensorFlow, and returns the clustered results.
- `/competitor_details` (POST) : Accepts JSON data containing a place ID and returns details about the specified competitor.
- `/top_competitors` (POST) : Accepts JSON data containing latitude and longitude, and returns the top competitors in the specified area.
- `/articles` (GET) : Returns a list of articles.

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
