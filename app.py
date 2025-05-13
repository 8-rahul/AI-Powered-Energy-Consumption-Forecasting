from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Load the trained MLP Regressor model (assuming it's saved as 'mlp_model.pkl')
model = joblib.load('energy_forecast_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract hour and day from the input data
        hour = data['hour']
        day = data['day']

        # Ensure inputs are valid
        if not (0 <= hour < 24):
            return jsonify({'error': 'Hour must be between 0 and 23'}), 400
        if not (0 <= day < 7):  # Assuming 0 = Sunday, 6 = Saturday
            return jsonify({'error': 'Day must be between 0 and 6'}), 400

        # Prepare the input array for prediction (e.g., [hour, day])
        input_data = np.array([[hour, day]])

        # Make prediction using the MLP model
        prediction = model.predict(input_data)

        # Return the prediction as a JSON response
        return jsonify({'predicted_energy': int(round(prediction[0]))})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)