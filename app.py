from flask import Flask, jsonify, request
from flask_swagger import swagger

app = Flask(__name__)


@app.route('/sum', methods=['POST'])
def sum_numbers():
    '''
    Retrieves the hello text
    ---
    tags:
      - math
    parameters:
      - in: body
        name: body
        schema:
          id: SumRequest
          required:
            - numbers
          properties:
            numbers:
              type: string
              description: comma seperated list of integers to sum
    responses:
      200:
        description: Your numbers were summed!
    '''
    numbers = [int(x) for x in request.json['numbers'].split(',')]
    result = {'result': sum(numbers)}
    return jsonify(result)


@app.route('/div', methods=['GET', 'POST'])
def div_numbers():
    '''
    Divide the two numbers given
    ---
    tags:
      - math
    parameters:
      - in: query
        name: numerator
        type: integer
        description: Numerator of the fraction
        required: yes
      - in: query
        name: denominator
        type: integer
        description: Denominator of the fraction
        required: yes
      - in: query
        name: use_float
        type: boolean
        description: if false, division will be integer truncation division
        default: true
    responses:
      200:
        description: Your result was calculated
      400:
        description: Bad inputs
      401:
        description: Only Chuck Norris can divide by zero
    '''
    numer = int(request.args.get('numerator') or request.form['numerator'])
    denom = int(request.args.get('denominator') or request.form['denominator'])
    use_float = request.args.get('use_float')
    if denom == 0:
        return 401
    if use_float is None or use_float.lower() != 'false':
        denom = float(denom)
    result = numer / denom
    return jsonify({'result': result})


@app.route('/get_offers/<int:mid>/', methods=['POST'])
def get_available_offers(mid):
    '''
    Get offers available to an mCent member
    ---
    tags:
      - offers
    parameters:
      - in: path
        name: mid
        type: integer
        description: Unique Member Id
        required: true
      - in: query
        name: country
        type: string
        description: 2-letter country ISO code
        required: true
      - in: body
        name: body
        schema:
          id: OffersRequest
          required:
            - ip
          properties:
            ip:
              type: string
              description: ip address of the device
            weight:
              type: integer
              description: Your weight

    responses:
      200:
        description: Offers were retrieved for the member
    '''
    result = {
        'mid': mid,
        'country': request.args.get('country'),
        'ip': request.json.get('ip'),
        'wight': request.json.get('weight')
    }
    return jsonify(result)


@app.route('/spec')
def spec():
    return jsonify(swagger(app))

if __name__ == '__main__':
    app.run(debug=True)
