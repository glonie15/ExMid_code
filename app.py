from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Load crop data
with open('data/negros_crops.json') as f:
    crop_data = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    crops = []
    if request.method == 'POST' and 'exit' not in request.form:
        pH = float(request.form['ph'])
        soil_type = request.form['soil_type'].lower()
        moisture = request.form['moisture'].lower()

        print(f"User input - pH: {pH}, Soil: {soil_type}, Moisture: {moisture}")

        for crop in crop_data:
            print(f"Checking crop: {crop['crop']}")
            if (crop['pH_min'] <= pH <= crop['pH_max'] and
                crop['soil_type'] == soil_type and
                crop['moisture_level'].lower() == moisture):
                print(f"Match found: {crop['crop']}")
                harvest_date = datetime.today() + timedelta(days=crop['duration_days'])
                crop['harvest_date'] = harvest_date.strftime('%B %d, %Y')
                crops.append(crop)

        if not crops:
            print("No matching crops found.")

    elif request.method == 'POST' and 'exit' in request.form:
        return render_template('goodbye.html')

    return render_template('index.html', crops=crops)

if __name__ == '__main__':
    app.run(debug=True)
