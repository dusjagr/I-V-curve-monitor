# I-V Curve Monitor

A web-based visualization tool for I-V curves with power curve analysis. This application fetches data from ThingSpeak and displays both I-V and power curves with maximum power point tracking.

## Features

- Real-time I-V curve visualization
- Power curve calculation and display
- Maximum Power Point (MPP) tracking
- Responsive cyberpunk-themed design
- Key measurements display (Voc, Isc, MPP, FF)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure ThingSpeak credentials in `app.py`:
```python
CHANNEL_ID = "your_channel_id"
READ_API_KEY = "your_api_key"
```

3. Run the application:
```bash
python app.py
```

4. Open a web browser and navigate to `http://localhost:5000`

## Dependencies

- Flask
- Requests
- Chart.js
- Bootstrap
