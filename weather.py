from flask import Flask, request, jsonify
import requests
from flasgger import Swagger

app = Flask(__name__)
# Initialize Swagger
swagger = Swagger(app)

API_KEY = "bd5e378503939ddaee76f12ad7a97608"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
# YOUR_API_KEY" https://gist.github.com/lalithabacies/c8f973dc6754384d6cade282b64a8cb1
@app.route('/weather', methods=['GET'])
def get_weather_api():
    """
    Fetch real-time weather data for a specific city.
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
        description: The name of the city to get weather for.
    responses:
      200:
        description: Weather data retrieved successfully.
        schema:
          id: WeatherResponse
          properties:
            city:
              type: string
            temperature:
              type: number
            description:
              type: string
            humidity:
              type: integer
      400:
        description: Missing city parameter.
      404:
        description: City not found.
    """
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