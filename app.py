from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)
def is_prime(n):
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max_divisor = int(n ** 0.5) + 1
    for d in range(3, max_divisor, 2):
        if n % d == 0:
            return False
    return True
def is_perfect(n):
    """Check if a number is perfect"""
    if n <= 1:
        return False
    sum_divisors = 1
    max_divisor = int(n ** 0.5) + 1
    for d in range(2, max_divisor):
        if n % d == 0:
            sum_divisors += d
            if (other := n // d) != d:
                sum_divisors += other
    return sum_divisors == n
def digit_sum(n):
    """Calculate sum of digits"""
    return sum(int(d) for d in str(abs(n)))
def is_armstrong(n):
    """Check if a number is an Armstrong number"""
    if n < 0:
        return False
    num_str = str(n)
    num_digits = len(num_str)
    return n == sum(int(d) ** num_digits for d in num_str)
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Main classification endpoint"""
    number_param = request.args.get('number')
    # Input validation
    if not number_param:
        return jsonify({"number": None, "error": True}), 400
    try:
        num = int(number_param)
        if abs(num) > 10**8:
            return jsonify({
                "number": num,
                "error": "Number too large (max 100 million)"
            }), 400
    except ValueError:
        return jsonify({"number": number_param, "error": True}), 400
    properties = []
    try:
        properties.append('even' if num % 2 == 0 else 'odd')
        if is_prime(num):
            properties.append('prime')
        if is_perfect(num):
            properties.append('perfect')
        if is_armstrong(num):
            properties.append('armstrong')
    except Exception as e:
        app.logger.error(f"Error calculating properties: {str(e)}")
        return jsonify({
            "number": num,
            "error": "Error processing number"
        }), 500
    fun_fact = "No fun fact available"
    try:
        response = requests.get(
            f'http://numbersapi.com/{num}/math?json',
            timeout=3
        )
        response.raise_for_status()
        data = response.json()
        fun_fact = data.get('text', fun_fact)
    except requests.exceptions.RequestException as e:
        app.logger.warning(f"Numbers API error: {str(e)}")
    except ValueError as e:
        app.logger.warning(f"JSON decode error: {str(e)}")
    return jsonify({
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": digit_sum(num),
        "fun_fact": fun_fact
    })
if __name__ == '__main__':
    app.run()