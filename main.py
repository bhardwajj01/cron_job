from flask import Flask, request, jsonify
import re
app = Flask(__name__)

# Function to validate the International Phone Numbers
def is_valid_phone_number(phone_number):
    # Regex to check valid phone number.
    pattern = r"^[+]{1}(?:[0-9\\-\\(\\)\\/" \
              "\\.]\\s?){10,12}[0-9]{1}$"

    # If the phone number is empty, return false
    if not phone_number:
        return False

    # Return true if the phone number matched the Regex
    return bool(re.match(pattern, phone_number))

@app.route('/validate_phone', methods=['POST'])
def validate_phone():
    # Get phone number from both JSON and form data
    phone_number = request.form.get('phone_number')

    # Validate the phone number
    is_valid = is_valid_phone_number(phone_number)

    # Return an error if the phone number is not valid
    if not is_valid:
        return jsonify({'error': 'Not a valid phone number'}), 400

    # Prepare response for valid phone number
    response = {
        'phone_number': phone_number,
        'is_valid': is_valid,
        'message': 'Valid phone number'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
