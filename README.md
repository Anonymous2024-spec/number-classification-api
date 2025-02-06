# Number Classification API

## Description
This API classifies a given number by checking whether it is prime, perfect, an Armstrong number, and whether it is odd or even. It also computes the sum of its digits and fetches a fun fact about the number from Numbers API.

## API Endpoint
**GET** `/api/classify-number?number=<number>`

### Example Request
GET https://number-classification-api-73il.onrender.com/api/classify-number?number=371

### Example Response (200 OK)
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
Example Error Response (400 Bad Request)

{
    "number": "alphabet",
    "error": true,
    "message": "Invalid input. Please provide a valid integer."
}
Setup Instructions
Clone the repository:

git clone https://github.com/yourusername/number-classification-api.git
cd number-classification-api
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the dependencies:

pip install -r requirements.txt
Run the app:

python app.py
Access the API at: http://127.0.0.1:5000/api/classify-number?number=371
Deployment
This API is deployed at: https://number-classification-api-73il.onrender.com

Tech Stack
Language: Python
Framework: Flask
Deployment: Render
