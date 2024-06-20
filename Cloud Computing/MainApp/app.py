from flask import Flask, request, jsonify

import json

from method.nearbycompetitors import NearbyCompetitors
from method.responses import *
from method.articles import *

app = Flask(__name__)
service = NearbyCompetitors("gmapsapi-c4dca")
articles_service = Articles("gmapsapi-c4dca")

headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

@app.route('/modelling_results', methods=['POST'])
def modelling_results():
    
    try:
        request_json = request.get_json()
        arglatitude = request_json.get("arglatitude")
        arglongitude = request_json.get("arglongitude")

        if arglatitude is None or arglongitude is None:
            response = {
                "status": 400,
                "places": None,
                "message": "Tidak menemukan parameter JSON 'arglatitude' dan/atau 'arglongitude'"
            }
            return (json.dumps(response), 400, headers)

        # Add additional data type checks if needed
        if not isinstance(arglatitude, (float)) or not isinstance(arglongitude, (float)):
            response = {
                "status": 400,
                "places": None,
                "message": "'arglatitude' dan 'arglongitude' harus bertipe float64"
            }
            return (json.dumps(response), 400, headers)

        response = service.modelling(arglatitude, arglongitude)

        return (json.dumps(response), 200, headers)

    except Exception as e:
        internal_error(headers)


@app.route('/competitor_details', methods=['POST'])
def competitor_details():
    
    try:
        request_json = request.get_json()
        argplace_id = request_json.get("argplace_id")

        if argplace_id is None:
            response = {
                "status": 400,
                "details": None,
                "message": "Tidak menemukan parameter JSON 'argplace_id'"
            }
            return (json.dumps(response), 400, headers)

        response = service.get_competitor_details(argplace_id)

        if response["details"]==[]:
            not_found_error(headers)

        return (json.dumps(response), 200, headers)

    except Exception as e:
        internal_error(headers)

@app.route('/top_competitors', methods=['POST'])
def top_competitors():

    try:
        request_json = request.get_json()
        arglatitude = request_json.get("arglatitude")
        arglongitude = request_json.get("arglongitude")

        if arglatitude is None or arglongitude is None:
            response = {
                "status": 400,
                "places": None,
                "message": "Tidak menemukan parameter JSON 'arglatitude' dan/atau 'arglongitude'"
            }
            return (json.dumps(response), 400, headers)

        # Add additional data type checks if needed
        if not isinstance(arglatitude, (float)) or not isinstance(arglongitude, (float)):
            response = {
                "status": 400,
                "places": None,
                "message": "'arglatitude' dan 'arglongitude' harus bertipe float64"
            }
            return (json.dumps(response), 400, headers)

        response = service.get_top_competitors(arglatitude, arglongitude)

        return (json.dumps(response), 200, headers)

    except Exception as e:
        internal_error(headers)

@app.route('/articles', methods=['GET'])
def articles():

    try:
        response = articles_service.get_articles()
        
        return (json.dumps(response), 200, headers)

    except Exception as e:
        internal_error(headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
