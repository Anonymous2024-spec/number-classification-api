from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Utility Functions

def is_prime(n):
    """Return True if n is a prime number, else False."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_perfect(n):
    """Return True if n is a perfect number, else False."""
    if n < 2:
        return False
    # Calculate sum of proper divisors
    divisors_sum = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            divisors_sum += i
            if i != n // i:
                divisors_sum += n // i
        i += 1
    return divisors_sum == n

def is_armstrong(n):
    """Return True if n is an Armstrong number, else False."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def digit_sum(n):
    """Return the sum of digits of n."""
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n):
    """Retrieve a math fun fact about the number from the Numbers API."""
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "No fun fact available."
    except Exception as e:
        return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get 'number' parameter from query string
    num_str = request.args.get('number', '')
    
    # Validate the input: must be an integer
    try:
        num = int(num_str)
    except ValueError:
        return jsonify({
            "number": num_str,
            "error": True,
            "message": "Invalid input. Please provide a valid integer."
        }), 400

    # Compute properties
    prime = is_prime(num)
    perfect = is_perfect(num)
    armstrong = is_armstrong(num)
    ds = digit_sum(num)
    odd_or_even = "odd" if num % 2 != 0 else "even"
    
    # Build the properties array
    if armstrong:
        properties = ["armstrong", odd_or_even]
    else:
        properties = [odd_or_even]

    fun_fact = get_fun_fact(num)

    # Build the JSON response
    result = {
        "number": num,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": ds,
        "fun_fact": fun_fact
    }
    return jsonify(result), 200

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
