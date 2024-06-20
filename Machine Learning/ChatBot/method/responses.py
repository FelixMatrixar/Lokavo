import json

headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

def internal_error(headers=headers):
    """
    Create a standardized error response for the application.
    
    Parameters:
    status_code (int): The HTTP status code for the error response.
    message (str): A message describing the error.
    headers (dict): Optional HTTP headers to include in the response.
    
    Returns:
    tuple: A tuple containing the JSON response, status code, and headers.
    """
    response = {
        "status": 500,
        "places": None,
        "message": "Server mengalami kesalahan internal dan tidak dapat menyelesaikan permintaan Anda."
    }
    
    return json.dumps(response), 500, headers

def insufficient_competitors(count_of_places, headers=headers):
    """
    Create a standardized response for insufficient competitors.

    Parameters:
    count_of_places (int): The count of available competitors.
    headers (dict): Optional HTTP headers to include in the response.

    Returns:
    tuple: A tuple containing the JSON response, status code, and headers.
    """    
    response = {
        "status": 4001,
        "count": count_of_places,
        "places": None,
        "message": "Tidak tersedia kompetitor yang cukup untuk melakukan analisis."
    }

    return json.dumps(response), 400, headers

def not_found_error(headers=headers):
    """
    Create a standardized 404 error response for the application.
    
    Parameters:
    headers (dict): Optional HTTP headers to include in the response.
    
    Returns:
    tuple: A tuple containing the JSON response, status code, and headers.
    """
    response = {
        "status": 404,
        "details": None,
        "message": "Tidak tersedia"
    }
    
    return json.dumps(response), 404, headers

