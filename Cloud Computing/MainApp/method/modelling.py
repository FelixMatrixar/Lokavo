import json
import pandas as pd
import requests

from method.inferencing import *
from method.secret_config import PERFORM_CLUSTERING_URL

headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

def perform_clustering(df, clusters_n=3, iteration_n=100):
    # Select variable for clustering
    list_col = ['PC1', 'PC2', 'PC3']

    # Export the dataframe with selected variables to JSON format
    json_df = df[list_col].copy()
    json_df = json_df.apply(lambda row: row.to_dict(), axis=1).tolist()

    # Conduct Clustering Modelling from DynamicModelling Cloud Computing API
    url = PERFORM_CLUSTERING_URL
    clustering_result = requests.post(url, headers=headers, data=json.dumps({"dataframe": json_df}), timeout=100).json()["clustering_result"]
    
    # Convert the JSON format clustering result back to Pandas DataFrame
    clustering_result_df = [item["cluster"] for item in clustering_result]

    # Assign cluster to each row
    df["cluster"] = clustering_result_df

    # Create a mapping from specific numbers to letters
    num_to_letter = {0: 'A', 1: 'B', 2: 'C'}

    # Map the numeric clusters to letters
    df['cluster'] = df['cluster'].map(num_to_letter)
    
    # Describe descriptive statistics
    desc_stats_df = calculate_descriptive_stats(df.copy())
    
    # Get df
    return desc_stats_df, df

# def perform_clustering(df, num_clusters=3, num_iterations=100):
#     # Columns to use for clustering
#     clustering_columns = ['PC1', 'PC2', 'PC3']
    
#     # Create data points using the declared columns
#     points = df[clustering_columns].values
    
#     # Initialize KMeans
#     kmeans = KMeans(n_clusters=num_clusters, max_iter=num_iterations)
    
#     # Fit the model to the data
#     kmeans.fit(points)
    
#     # Get the cluster assignments
#     assignments = kmeans.labels_
    
#     # Save cluster results to the original DataFrame
#     df['cluster'] = assignments

#     # Create a mapping from specific numbers to letters
#     num_to_letter = {0: 'A', 1: 'B', 2: 'C'}

#     # Map the numeric clusters to letters
#     df['cluster'] = df['cluster'].map(num_to_letter)

#     # Describe descriptive statistics
#     desc_stats_df = calculate_descriptive_stats(df.copy())
    
#     # Get df
#     return desc_stats_df, df



