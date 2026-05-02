from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "your_openweathermap_api_key_here"  # Replace with your OpenWeatherMap API key
# https://gist.github.com/lalithabacies/c8f973dc6754384d6cade282b64a8cb1
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather_api():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
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
    app.run(debug=True)