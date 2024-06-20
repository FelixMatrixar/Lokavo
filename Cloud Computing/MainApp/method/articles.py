import json
import pandas as pd
import requests

from google.cloud import bigquery

from method.queries import GET_ARTICLES

class Articles:
    def __init__(self, project_id):
        self.client = bigquery.Client(project_id)

    def get_articles(self):

        # Define the query with parameter placeholders
        query = GET_ARTICLES

        # Execute the query
        query_job = self.client.query(query)
        results = query_job.result()
        
        rows = []
        for row in results:
            row_dict = dict(row.items())  # Convert Row to dict
            rows.append(row_dict)
        
        response = {
            "status": 200,
            "list": rows
        }
        return response