from flask import Flask, request, json, jsonify

import json
import logging
import uuid

from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from method.nearbycompetitors import NearbyCompetitors
from method.responses import *

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

service = NearbyCompetitors("capstone-project-ents-h110")

headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

# In-memory storage for UUID and responses
responses_store = {}

# Function to write the response to a markdown file
def write_to_md(response, filename, instruction_prompt):
    with open(filename, 'w') as file:
        file.write(f"Topik : Analisa ulasan kritik atau saran dari konsumen kompetitor\n\n")
        file.write(f"{instruction_prompt}\n\n")
        for detail in response["details"]:
            file.write(f"- {detail['english_review']}\n\n")
        file.write("Jangan berikan saran dan kesimpulan terlebih dahulu. \n\n")

# Function to download file from Google Cloud Storage
def download_from_gcs(bucket_name, source_blob_name):
    """Downloads a file from the bucket."""
    storage_client = storage.Client("capstone-project-ents-h110")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    content = blob.download_as_text()
    return content

# Function to upload file to Google Cloud Storage
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client("capstone-project-ents-h110")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

@app.route('/chatbot', methods=['POST'])
def chatbot():
    headers = {'Content-Type': 'application/json'}
    
    try:
        request_json = request.get_json()
        logging.debug(f"Received JSON request: {request_json}")

        arglatitude = request_json.get("arglatitude")
        arglongitude = request_json.get("arglongitude")
        user_uuid = request_json.get("uuid")

        logging.debug(f"Extracted parameters - arglatitude: {arglatitude}, arglongitude: {arglongitude}, uuid: {user_uuid}")

        if arglatitude is None or arglongitude is None or user_uuid is None:
            response = {
                "status": 400,
                "places": None,
                "message": "Tidak menemukan parameter JSON 'arglatitude', 'arglongitude', dan/atau 'uuid'"
            }
            logging.warning("Missing 'arglatitude', 'arglongitude', and/or 'uuid' in the request")
            return (json.dumps(response), 400, headers)
        
        # Add additional data type checks if needed
        if not isinstance(arglatitude, float) or not isinstance(arglongitude, float) or not isinstance(user_uuid, str):
            response = {
                "status": 400,
                "places": None,
                "message": "'arglatitude' dan 'arglongitude' harus bertipe float64, dan 'uuid' harus bertipe string"
            }
            logging.warning("'arglatitude' and/or 'arglongitude' are not of type float64, or 'uuid' is not of type string")
            return (json.dumps(response), 400, headers)

        # # Validate UUID format
        # try:
        #     uuid.UUID(user_uui/
        # d)
        # except ValueError:
        #     response = {
        #         "status": 400,
        #         "places": None,
        #         "message": "'uuid' tidak valid"
        #     }
        #     logging.warning("'uuid' is not valid")
        #     return (json.dumps(response), 400, headers)

        # Assuming service.get_reviews is a defined function elsewhere in your code
        response = service.get_reviews(arglatitude, arglongitude)

        md_filenames = [
            f'feedback_priority_1_{user_uuid}.md',
            f'feedback_priority_2_{user_uuid}.md',
            f'feedback_priority_3_{user_uuid}.md'
        ]
        instruction_prompts = [
            "Terjemahkanlah beberapa ulasan konsumen kompetitor ini ke dalam Bahasa Indonesia yang enak dibaca dalam paragraf",
            "Simpulkanlah secara ringkas ulasan-ulasan konsumen kompetitor ini ke dalam Bahasa Indonesia yang enak dibaca tentang faktor kritikan dari konsumen kompetitor dalam 350 karakter paragraf.",
            "Jelaskan apa yang bisa dilakukan oleh orang yang ingin membuka bisnis dengan mempertimbangkan ulasan-ulasan kritikan konsumen kompetitor."
        ]

        # Store responses in the in-memory storage
        responses_store[user_uuid] = {
            "1": None,
            "2": None,
            "3": None
        }

        # Use ThreadPoolExecutor to run tasks in parallel
        with ThreadPoolExecutor() as executor:
            futures = []
            for idx, (md_filename, instruction_prompt) in enumerate(zip(md_filenames, instruction_prompts), 1):
                futures.append(executor.submit(write_to_md, response, md_filename, instruction_prompt))
                futures.append(executor.submit(upload_to_gcs, 'feedback_priority', md_filename, md_filename))
                # Update in-memory store with the filename (or any other required info)
                responses_store[user_uuid][str(idx)] = md_filename

            # Wait for all futures to complete
            for future in futures:
                future.result()

        return jsonify({"uuid": user_uuid, "status": "processing"}), 200, headers

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        response = {
            "status": 500,
            "places": None,
            "message": "Internal server error"
        }
        return (json.dumps(response), 500, headers)

@app.route('/chatbot/<uuid>/<int:type>', methods=['GET'])
def get_response(uuid, type):
    if uuid in responses_store and str(type) in responses_store[uuid]:
        filename = responses_store[uuid][str(type)]
        if filename:
            content = download_from_gcs('feedback_priority-summaries', filename)
            
            # Define questions based on type
            questions = {
                1: "Apa saja kritikan dan saran dari konsumen kompetitor?",
                2: "Apa kesimpulannya?",
                3: "Apa yang bisa saya lakukan?"
            }
            
            # Get the corresponding question
            question = questions.get(type, "Question not found")

            return jsonify({"question": question, "answer": content}), 200
        else:
            return jsonify({"error": "Result is not ready yet."}), 202
    else:
        return jsonify({"error": "Invalid UUID or type."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)