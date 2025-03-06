from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)

# Get ThingSpeak credentials from environment variables
CHANNEL_ID = os.getenv('THINGSPEAK_CHANNEL_ID', '2860934')
READ_API_KEY = os.getenv('THINGSPEAK_READ_API_KEY', 'MA2OFWB36S4YOVUP')
THINGSPEAK_BASE_URL = "https://api.thingspeak.com/channels"
ZURICH_TZ = pytz.timezone('Europe/Zurich')

def get_thingspeak_data(hours=24):
    """Get data from ThingSpeak channel"""
    try:
        url = f"{THINGSPEAK_BASE_URL}/{CHANNEL_ID}/feeds.json"
        params = {
            'api_key': READ_API_KEY,
            'results': 1  # We only need the latest measurement
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching ThingSpeak data: {e}")
        return None

def process_thingspeak_data(data):
    """Process ThingSpeak data into a format suitable for charts"""
    if not data or 'feeds' not in data:
        return []
        
    measurements = []
    for feed in data['feeds']:
        try:
            timestamp = datetime.strptime(feed['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            timestamp = pytz.utc.localize(timestamp)
            local_time = timestamp.astimezone(ZURICH_TZ)
            
            # Extract I-V curve data
            voltage_str = feed.get('field5', '')
            current_str = feed.get('field6', '')
            
            # Convert voltage from mV to V
            voltage_values = [float(v)/1000 for v in voltage_str.split(',') if v]
            current_values = [float(i) for i in current_str.split(',') if i]
            
            # Convert units appropriately
            voc = float(feed.get('field1', 0))/1000  # Convert mV to V
            isc = float(feed.get('field2', 0))       # Already in mA
            mpp = float(feed.get('field3', 0))/1000  # Convert to mW
            ff = float(feed.get('field4', 0))        # No conversion needed
            
            measurements.append({
                'timestamp': local_time.strftime('%Y-%m-%d %H:%M:%S'),
                'entry_id': feed.get('entry_id', 'N/A'),
                'voc': voc,
                'isc': isc,
                'mpp': mpp,
                'ff': ff,
                'voltage_values': voltage_values,
                'current_values': current_values
            })
        except (ValueError, TypeError) as e:
            print(f"Error processing data: {e}")
            continue
    
    return measurements

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get the latest sensor data"""
    try:
        data = get_thingspeak_data()
        if data:
            processed_data = process_thingspeak_data(data)
            return jsonify({
                'success': True,
                'data': processed_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch data from ThingSpeak'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
