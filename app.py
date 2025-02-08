from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)
def is_prime(n):
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
    if n <= 1:
        return False
    sum_divisors = 1
    max_divisor = int(n ** 0.5) + 1
    for d in range(2, max_divisor):
        if n % d == 0:
            sum_divisors += d
            other = n // d
            if other != d:
                sum_divisors += other
    return sum_divisors == n
def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))
def is_armstrong(n):
    if n < 0:
        return False
    num_str = str(n)
    num_digits = len(num_str)
    sum_powers = sum(int(d) ** num_digits for d in num_str)
    return sum_powers == n
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number')
    if not number_param:
        return jsonify({"number": None, "error": True}), 400
    try:
        num = int(number_param)
    except ValueError:
        return jsonify({"number": number_param, "error": True}), 400
    properties = []
    if num % 2 == 0:
        properties.append('even')
    else:
        properties.append('odd')
    if is_prime(num):
        properties.append('prime')
    if is_perfect(num):
        properties.append('perfect')
    if is_armstrong(num):
        properties.append('armstrong')
    fun_fact = 'No fun fact available.'
    try:
        response = requests.get(f'http://numbersapi.com/{num}/math?json', timeout=3)
        if response.status_code == 200:
            data = response.json()
            fun_fact = data.get('text', fun_fact)
    except requests.exceptions.RequestException:
        pass
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