from flask import Flask, request, jsonify

import json
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

# Clustering function with TensorFlow
def update_centroids(points, assignments, clusters_n):
    means = []
    for c in range(clusters_n):
        cluster_points = tf.gather(points, tf.reshape(tf.where(tf.equal(assignments, c)), [-1]))
        mean = tf.reduce_mean(cluster_points, axis=0)
        means.append(mean)
    return tf.stack(means)

@app.route('/perform_clustering', methods=['POST'])
def perform_clustering():
    try:
        data = request.get_json()  # Receiving JSON Parameter

        df = pd.DataFrame(data.get("dataframe"))  # Assuming dataframe is sent as 'dataframe' key

        # Clustering parameters
        clusters_n = data.get('clusters_n', 3)
        iteration_n = data.get('iteration_n', 100)
        list_col = ['PC1', 'PC2', 'PC3']  # Assuming these are the columns for clustering

        # Convert DataFrame to TensorFlow-compatible array
        points = df[list_col].values

        # Create initial centroids
        centroids = tf.Variable(tf.slice(tf.random.shuffle(points), [0, 0], [clusters_n, -1]))

        # K-means algorithm
        for step in range(iteration_n):
            points_expanded = tf.expand_dims(points, 0)
            centroids_expanded = tf.expand_dims(centroids, 1)

            distances = tf.reduce_sum(tf.square(points_expanded - centroids_expanded), axis=2)
            assignments = tf.argmin(distances, axis=0)

            new_centroids = update_centroids(points, assignments, clusters_n)
            centroids.assign(new_centroids)

        # Assign clusters to the original DataFrame
        df['cluster'] = assignments.numpy()

        # Drop PCs
        df.drop(columns=list_col, axis=1, inplace=True)

        # Return clustered DataFrame
        return ({"clustering_result": df.to_dict(orient='records')})
    
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500  # Return error message with status code 500 (Internal Server Error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
