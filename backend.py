from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend.html (opened as a local file) to call this API

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    num1 = data.get('num1')
    num2 = data.get('num2')
    operation = data.get('operation')
    allowed_operations = ['add', 'sub', 'mul', 'div', 'sqrt', 'pow']

    if operation not in allowed_operations:
        return jsonify({
            "ERROR": "Invalid operation choice.",
            "Message": "The correct operations are: add, sub, mul, div, sqrt, pow."
        }), 400

    # sqrt only needs num1, everything else needs num1 and num2
    try:
        num1 = float(num1)
        if operation != 'sqrt':
            num2 = float(num2)
    except (TypeError, ValueError):
        return jsonify({"ERROR": "num1 and num2 must be valid numbers"}), 400

    if operation == 'add':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mul':
        result = num1 * num2
    elif operation == 'div':
        if num2 == 0:
            return jsonify({"ERROR": "Cannot divide by zero"}), 400
        result = num1 / num2
    elif operation == 'sqrt':
        if num1 < 0:
            return jsonify({"ERROR": "Cannot take square root of a negative number"}), 400
        result = num1 ** 0.5
    elif operation == 'pow':
        result = num1 ** num2

    # return whole numbers as ints instead of floats (5.0 -> 5)
    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)