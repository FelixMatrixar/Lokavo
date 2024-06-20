import json
import pandas as pd
import requests

from google.cloud import bigquery
from method.modelling import *
from method.preprocessing import *
from method.queries import *
from method.responses import *
from method.visualizing import *
from method.secret_config import GEMINI_URL

class NearbyCompetitors:
    def __init__(self, project_id):
        self.client = bigquery.Client(project_id)

    def modelling(self, arglatitude, arglongitude):
        count_of_places = self.get_business_count(arglatitude, arglongitude)

        if count_of_places < 30:
            # insufficient_competitors(count_of_places)
            return {
                "status": 4001,
                "count": count_of_places,
                "message": "Tidak tersedia kompetitor yang cukup untuk melakukan analisis."
            }

        query = GET_COMPETITORS_QUERY

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("arglatitude", "FLOAT64", arglatitude),
                bigquery.ScalarQueryParameter("arglongitude", "FLOAT64", arglongitude),
            ]
        )

        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()

        rows = []
        for row in results:
            row_dict = dict(row)
            
            # Correct the coordinates field
            row_dict['coordinates'] = json.loads(row_dict['coordinates'])
            
            # Correct the reviews_per_rating field
            row_dict['reviews_per_rating'] = json.loads(row_dict['reviews_per_rating'])

            rows.append(row_dict)
        
        # Convert to Pandas DataFrame
        df = pd.DataFrame(rows)
        
        # Split Reviews per Rating
        df = split_reviews_per_rating(df)
        
        # Impute
        df = impute(df)

        # Normalization and PCA Transformation
        df = pca(df)
        
        # Modelling
        desc_stats_df, df = perform_clustering(df)
        
        # What POI to Show on Map
        poi = show_on_map(df).to_dict(orient='records')

        # Cluster Proportion
        cluster_count_dict = dict(zip(desc_stats_df[('cluster', '')], desc_stats_df[('place_id', 'count')]))
        cluster_counts = df['cluster'].value_counts() # For further inferencing    

        # Drop PCs to Free Some Memories
        df.drop(columns=["PC1", "PC2", "PC3"], axis=1, inplace=True)

        # Get Summary Header (Fairly Competitive or Highly Competitive)
        summary_header = summary_heading(cluster_counts)

        # Dynamically Generate Prompts
        stats_prompt = generate_cluster_summary(desc_stats_df)
        full_prompt = text_modelling(stats_prompt)
        
        # proportion_stats_prompt = generate_cluster_proportion_summary(cluster_counts)
        # full_small_prompt = small_text_modelling(summary_header, proportion_stats_prompt)

        # Answer from Gemini
        answer = requests.post(GEMINI_URL, headers=headers, data=json.dumps({"prompt": full_prompt}), timeout=100)
        # brief_answer = requests.post(GEMINI_URL, headers=headers, data=json.dumps({"prompt": full_small_prompt}), timeout=100)

        return {
            "status": 200,
            "count": count_of_places,
            "summary_header": summary_header,
            # "short_interpretation": brief_answer.json()["response_text"],
            "cluster_proportion": cluster_count_dict,
            "cluster_interpretation": generate_cluster_meaning(desc_stats_df),
            "long_interpretation": answer.json()["response_text"],
            "poi_map": poi,
        }
        
    def get_competitor_details(self, argplace_id):
        # Define the query with parameter placeholders
        query = GET_COMPETITOR_DETAILS_QUERY

        # Configure the query with parameters
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("argplace_id", "STRING", argplace_id),
            ]
        )

        # Execute the query
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()

        rows = []
        for row in results:
            row_dict = dict(row)
            
            # Correct the coordinates field
            row_dict['coordinates'] = json.loads(row_dict['coordinates'])

            # Correct the categories field
            row_dict['categories'] = json.loads(row_dict['categories'])

            # Correct the most_popular_times field
            if row_dict['most_popular_times'] is not None:
                row_dict['most_popular_times'] = json.loads(row_dict['most_popular_times'])
            
            # Correct the reviews_per_rating field
            row_dict['reviews_per_rating'] = json.loads(row_dict['reviews_per_rating'])

            rows.append(row_dict)

        # Construct the final response
        response = {
            "status": 200,
            "details": rows
        }

        return response

    def get_top_competitors(self, arglatitude, arglongitude):
        query = GET_TOP_COMPETITORS

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("arglatitude", "FLOAT64", arglatitude),
                bigquery.ScalarQueryParameter("arglongitude", "FLOAT64", arglongitude),
            ]
        )

        query_job = self.client.query(query, job_config=job_config)
        count_results = query_job.result()
        rows = []
        for row in count_results:
            row_dict = dict(row)
            
            # Correct the coordinates field
            row_dict['coordinates'] = json.loads(row_dict['coordinates'])

            rows.append(row_dict)
        
        # Construct the final response
        response = {
            "status": 200,
            "details": rows
        }

        return response

    def get_business_count(self, arglatitude, arglongitude):
        
        query = COUNT_BUSINESSES_QUERY

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("arglatitude", "FLOAT64", arglatitude),
                bigquery.ScalarQueryParameter("arglongitude", "FLOAT64", arglongitude),
            ]
        )

        query_job = self.client.query(query, job_config=job_config)
        count_results = query_job.result()
        rows = []
        for row in count_results:
            row_dict = dict(row)
            rows.append(row_dict)
        
        count_of_places = rows[0]['count_of_places_within_4km']
        # count_row = list(count_results)[0]
        # count_of_places = count_row["count_of_places_within_4km"]

        return count_of_places
            