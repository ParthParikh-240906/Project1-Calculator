from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods = ['POST'])
def calculate():
    data = request.get_json()

    num1 = data.get('num1')
    num2 = data.get('num2')
    operation = data.get('operation')
    allowed_operations = ['add', 'sub', 'mul', 'div', 'sqrt', 'pow']

    try:
        num1 = float(num1)
        num2 = float(num2)
    except (TypeError, ValueError):
        return jsonify({"ERROR": "num1 and num2 must be valid numbers"}), 400

    if operation not in allowed_operations:
        return jsonify({
            "ERROR": "Invalid operation choice.",
            "Message": "The correct operations are: add, sub, mul, div, sqrt, pow."
        }), 400
    elif operation == 'add' :
        result = num1 + num2
    elif operation == 'sub' :
        result = num1 - num2
    elif operation == 'mul' :
        result = num1 * num2
    elif operation == 'div' :
        if num2 == 0:
            return jsonify({"ERROR": "Cannot divide by zero"}),400
        result = num1 / num2
    elif operation == 'sqrt' :
        if num2 is None :
            result = num1 ** 0.5
        else :
            result = [num1 ** 0.5 , num2 ** 0.5]
    elif operation == 'pow' :
        result = num1 ** num2
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
