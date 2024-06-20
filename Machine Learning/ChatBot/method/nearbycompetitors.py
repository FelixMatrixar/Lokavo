import json
import pandas as pd
import requests

from google.cloud import bigquery
from method.queries import *

class NearbyCompetitors:
    def __init__(self, project_id):
        self.client = bigquery.Client(project_id)
    
    def get_reviews(self, arglatitude, arglongitude):
        # Define the query with parameter placeholders
        query = GET_PRIORITY_REVIEWS

        # Configure the query with parameters
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("arglatitude", "FLOAT64", arglatitude),
                bigquery.ScalarQueryParameter("arglongitude", "FLOAT64", arglongitude),
            ]
        )


        # Execute the query
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()

        rows = []
        for row in results:
            row_dict = dict(row)
            
            rows.append(row_dict)

        # Construct the final response
        response = {
            "status": 200,
            "details": rows
        }

        return response