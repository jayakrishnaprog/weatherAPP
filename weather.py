from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual OpenWeatherMap API key
API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather_api():
    # Get the 'city' parameter from the URL (e.g., /weather?city=London)
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    try:
        # Fetching data as described in the weather app concept
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extracting relevant JSON data for a user-friendly format
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"]
            }
            return jsonify(weather_data), 200
        else:
            return jsonify({"error": data.get("message", "City not found")}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Runs the app on http://127.0.0.1:5000
    app.run(debug=True)