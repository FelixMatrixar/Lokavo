# Project Description

This project demonstrates a Flask-based API for dynamic clustering using TensorFlow, with a demo of input and clustering results.

## Table of Contents

- [Introduction](#introduction)
- [File Structure](#file-structure)
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)
- [License](#license)

## Introduction

This repository contains a Flask application that performs dynamic clustering using TensorFlow. It accepts JSON data containing a dataframe as input, performs clustering based on specified parameters, and returns the clustered results.

## File Structure

app.py # Main application file <br>
demo.py # Demonstration of the API <br>
demo_input.json # Example JSON input for POST request <br>
demo_results.json # Example JSON output demonstrating clustering results <br>
requirements.txt # File listing dependencies <br>

- `app.py`: Main Flask application file that implements dynamic clustering using TensorFlow.
- `demo.py`: Script demonstrating how to interact with the API using example input (`demo_input.json`) and showcasing the clustering results (`demo_results.json`).
- `requirements.txt`: List of Python packages required to run the application.

## Endpoints

`/perform_clustering` (POST) : Accepts JSON data containing a dataframe and performs dynamic clustering using TensorFlow.

## Dependencies

- Flask (3.0.\*)
- functions-framework (3.\*)
- pandas (2.2.\*)
- tensorflow (2.16.\*)
- gunicorn

## License

MIT License
