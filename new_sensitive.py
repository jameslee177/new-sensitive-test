from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import json
import logging

app = Flask(__name__)
api = Api(app, version='1.0', title='Login API',
          description='API for user login.')

# Load user data from an external JSON file
with open('mock_users.json', 'r') as f:
    mock_users = json.load(f)["users"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the request body model
login_model = api.model('Login', {
    'email': fields.String(
        required=True,
        description="User's email address",
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
        example="user@example.com"
    ),
    'password': fields.String(
        required=True,
        description="User's password",
        example="mypassword123"
    )
})

# Define the response model
user_response_model = api.model('UserResponse', {
    'id': fields.Integer(description="User ID"),
    'name': fields.String(description="User's name"),
    'email': fields.String(description="User's email address"),
})

error_response_model = api.model('ErrorResponse', {
    'error': fields.String(description="Error message")
})

@api.route('/anything/api/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Success', user_response_model)
    @api.response(400, 'Invalid Input or Credentials', error_response_model)
    def post(self):
        """
        Logs the user in with email and password.
        """
        input_data = request.json or {}
        email = input_data.get('email')
        password = input_data.get('password')

        # Check for missing input
        if not email or not password:
            return {"error": "Missing input"}, 400

        # Simulate database query from external data
        user = mock_users.get(email)

        # Validate user and password
        if not user or user["password"] != password:
            return {"error": "Invalid login credentials"}, 400

        # Log the successful login
        logger.info(f"LOGIN OK: User '{email}' logged in successfully. Agent: {request.headers.get('User-Agent')}")

        # Exclude sensitive fields like password before returning user info
        user_response = {key: value for key, value in user.items() if key != "password"}
        return user_response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
