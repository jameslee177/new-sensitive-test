from flask import Flask, jsonify, request
import json
import logging
import re

app = Flask(__name__)

# Load user data from an external JSON file
with open('mock_users.json', 'r') as f:
    mock_users = json.load(f)["users"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/anything/api/login', methods=['POST'])
def login():
    """
    Logs the user in with email and password.
    The request body must include:
    - email: A valid email address (string).
    - password: The user's password (string).

    Responses:
    - 200: JSON object with user information (excluding sensitive fields).
    - 400: JSON object with an error message.
    """
    input_data = request.json or {}

    # Validate input data
    email = input_data.get('email')
    password = input_data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing input"}), 400

    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return jsonify({"error": "Invalid email format"}), 400

    # Simulate database query from external data
    user = mock_users.get(email)

    # Validate user and password
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid login credentials"}), 400

    # Log the successful login
    logger.info(f"LOGIN OK: User '{email}' logged in successfully. Agent: {request.headers.get('User-Agent')}")

    # Exclude sensitive fields like password before returning user info
    user_response = {key: value for key, value in user.items() if key != "password"}
    return jsonify(user_response), 200


# Define a helper route to provide API schema (manual OpenAPI-like description)
@app.route('/anything/api/schema', methods=['GET'])
def api_schema():
    """
    Returns a manual API schema for tools that don't support auto-generation.
    """
    schema = {
        "paths": {
            "/anything/api/login": {
                "post": {
                    "description": "Logs the user in with email and password.",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {
                                            "type": "string",
                                            "description": "User's email address",
                                            "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                                        },
                                        "password": {
                                            "type": "string",
                                            "description": "User's password"
                                        }
                                    },
                                    "required": ["email", "password"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful login",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "name": {"type": "string"},
                                            "email": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Error response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(schema)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
