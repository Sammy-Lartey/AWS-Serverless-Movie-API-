import json
import boto3
import urllib.parse
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Movies")  # Ensure this table exists

def lambda_handler(event, context):
    """Handles API requests"""
    http_method = event.get("httpMethod", "")
    path_parameters = event.get("pathParameters", {})

    if http_method == "GET" and event.get("path", "") == "/movies":
        return get_movies()
    elif http_method == "POST" and event.get("path", "") == "/movies":
        return add_movie(json.loads(event.get("body", "{}")))
    elif http_method == "DELETE" and "title" in path_parameters:
        title = urllib.parse.unquote(path_parameters["title"])  # Decode URL-encoded titles
        return remove_movie(title)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid request"}),
            "headers": {"Content-Type": "application/json"}
        }

def format_data(obj):
    """Recursively converts Decimals and ensures 'year' & 'rating' are strings"""
    if isinstance(obj, list):
        return [format_data(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: str(v) if k in ["year", "rating"] else format_data(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return str(obj)  # Convert all decimals to strings
    return obj

def get_movies():
    """Retrieve all movies from DynamoDB"""
    response = table.scan()
    items = response.get("Items", [])
    return {
        "statusCode": 200,
        "body": json.dumps(format_data(items)),  # Convert Decimals properly
        "headers": {"Content-Type": "application/json"}
    }

def add_movie(data):
    """Add a movie to the library"""
    required_fields = {"Title", "director", "year", "rating"}
    if not required_fields.issubset(data):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required fields"}),
            "headers": {"Content-Type": "application/json"}
        }

    # Ensure year and rating are stored as strings
    data["year"] = str(data["year"])
    data["rating"] = str(data["rating"])

    table.put_item(Item=data)
    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Movie added successfully"}),
        "headers": {"Content-Type": "application/json"}
    }

def remove_movie(title):
    """Remove a movie from the library, but first check if it exists"""
    # Check if the movie exists before deleting
    response = table.get_item(Key={"Title": title})

    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Movie not found"}),
            "headers": {"Content-Type": "application/json"}
        }

    # Delete the movie
    table.delete_item(Key={"Title": title})
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"'{title}' removed successfully"}),
        "headers": {"Content-Type": "application/json"}
    }
