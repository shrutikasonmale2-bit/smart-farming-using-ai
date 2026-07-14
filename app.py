from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Smart Farming AI Model (Simplified ML)
class SmartFarmingAI:
    def __init__(self):
        self.soil_moisture_threshold = 40
        self.temperature_optimal = (22, 28)
        self.humidity_optimal = (60, 80)
        
    def predict_crop_health(self, soil_moisture, temperature, humidity, rainfall):
        """Predict crop health based on environmental factors"""
        health_score = 100
        recommendations = []
        
        # Soil Moisture Analysis
        if soil_moisture < self.soil_moisture_threshold:
            health_score -= 30
            recommendations.append("⚠️ IRRIGATION NEEDED: Soil moisture is low. Water your crops!")
        elif soil_moisture > 80:
            health_score -= 15
            recommendations.append("⚠️ EXCESS MOISTURE: Risk of root rot. Improve drainage!")
        else:
            recommendations.append("✅ Soil moisture is optimal")
        
        # Temperature Analysis
        if temperature < self.temperature_optimal[0]:
            health_score -= 20
            recommendations.append(f"⚠️ COLD ALERT: Temperature is too low (< {self.temperature_optimal[0]}°C)")
        elif temperature > self.temperature_optimal[1]:
            health_score -= 20
            recommendations.append(f"⚠️ HEAT ALERT: Temperature is too high (> {self.temperature_optimal[1]}°C)")
        else:
            recommendations.append("✅ Temperature is in optimal range")
        
        # Humidity Analysis
        if humidity < self.humidity_optimal[0]:
            health_score -= 15
            recommendations.append(f"⚠️ LOW HUMIDITY: Increase moisture in air (< {self.humidity_optimal[0]}%)")
        elif humidity > self.humidity_optimal[1]:
            health_score -= 15
            recommendations.append(f"⚠️ HIGH HUMIDITY: Risk of fungal diseases (> {self.humidity_optimal[1]}%)")
        else:
            recommendations.append("✅ Humidity levels are healthy")
        
        # Rainfall Analysis
        if rainfall < 20:
            recommendations.append(f"⚠️ LOW RAINFALL: Only {rainfall}mm. Consider irrigation!")
        elif rainfall > 100:
            recommendations.append(f"⚠️ HEAVY RAINFALL: {rainfall}mm. Risk of flooding!")
        else:
            recommendations.append(f"✅ Rainfall ({rainfall}mm) is adequate")
        
        health_score = max(0, min(100, health_score))
        
        return {
            "health_score": health_score,
            "recommendations": recommendations,
            "status": "Healthy" if health_score > 70 else "Warning" if health_score > 40 else "Critical"
        }
    
    def predict_pest_risk(self, temperature, humidity):
        """Predict pest risk based on climate conditions"""
        pest_risk = 0
        pest_alerts = []
        
        # Pest thrives in warm, humid conditions
        if 20 <= temperature <= 30 and humidity > 70:
            pest_risk = 80
            pest_alerts.append("🐛 HIGH PEST RISK: Warm and humid - ideal for pests!")
        elif 15 <= temperature <= 25 and humidity > 60:
            pest_risk = 50
            pest_alerts.append("🐛 MODERATE PEST RISK: Conditions favor pest growth")
        else:
            pest_risk = 20
            pest_alerts.append("✅ LOW PEST RISK: Current conditions limit pest activity")
        
        return {"pest_risk": pest_risk, "alerts": pest_alerts}
    
    def generate_watering_schedule(self, soil_moisture, temperature):
        """Generate optimal watering schedule"""
        if soil_moisture < 30:
            frequency = "Immediately"
            amount = "High (50mm)"
        elif soil_moisture < 50:
            frequency = "Daily"
            amount = "Medium (25mm)"
        else:
            frequency = "Every 2-3 days"
            amount = "Light (10mm)"
        
        return {"frequency": frequency, "amount": amount}

# Initialize AI Model
ai_model = SmartFarmingAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze farm conditions"""
    data = request.json
    
    soil_moisture = float(data.get('soil_moisture', 50))
    temperature = float(data.get('temperature', 25))
    humidity = float(data.get('humidity', 70))
    rainfall = float(data.get('rainfall', 50))
    
    # Get predictions
    crop_health = ai_model.predict_crop_health(soil_moisture, temperature, humidity, rainfall)
    pest_risk = ai_model.predict_pest_risk(temperature, humidity)
    watering = ai_model.generate_watering_schedule(soil_moisture, temperature)
    
    return jsonify({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": {
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        },
        "crop_health": crop_health,
        "pest_risk": pest_risk,
        "watering_schedule": watering
    })

@app.route('/api/forecast', methods=['GET'])
def forecast():
    """Get 7-day weather forecast"""
    forecast_data = []
    
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        temp = np.random.randint(20, 32)
        humidity = np.random.randint(55, 85)
        rainfall = np.random.randint(0, 80)
        
        forecast_data.append({
            "date": date,
            "temperature": temp,
            "humidity": humidity,
            "rainfall": rainfall,
            "condition": ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"][np.random.randint(0, 4)]
        })
    
    return jsonify({"forecast": forecast_data})

@app.route('/api/crop-suggestions', methods=['GET'])
def crop_suggestions():
    """Get crop suggestions based on season"""
    suggestions = {
        "Spring": ["Wheat", "Barley", "Peas", "Corn"],
        "Summer": ["Rice", "Cotton", "Sugarcane", "Maize"],
        "Autumn": ["Soybeans", "Groundnuts", "Chickpeas", "Lentils"],
        "Winter": ["Mustard", "Potatoes", "Onions", "Garlic"]
    }
    
    current_month = datetime.now().month
    if 3 <= current_month <= 5:
        season = "Spring"
    elif 6 <= current_month <= 8:
        season = "Summer"
    elif 9 <= current_month <= 11:
        season = "Autumn"
    else:
        season = "Winter"
    
    return jsonify({
        "season": season,
        "crops": suggestions[season],
        "tips": f"These crops are ideal for {season}. Ensure proper irrigation and pest management."
    })

@app.route('/api/disease-detection', methods=['POST'])
def disease_detection():
    """Simple disease detection based on conditions"""
    data = request.json
    temperature = float(data.get('temperature', 25))
    humidity = float(data.get('humidity', 70))
    
    diseases = []
    
    if humidity > 75 and temperature > 25:
        diseases.append("🍂 Fungal Infection Risk: High humidity + warm temp")
    if humidity < 40:
        diseases.append("🌾 Powdery Mildew Risk: Low humidity environments")
    if temperature < 15:
        diseases.append("❄️ Frost Damage Risk: Temperatures below freezing")
    
    if not diseases:
        diseases.append("✅ No major disease risks detected")
    
    return jsonify({"diseases": diseases})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
