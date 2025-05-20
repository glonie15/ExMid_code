from flask import Flask, render_template, request, redirect, url_for, flash
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flash messages

# Load crop data
with open('data/negros_crops.json', 'r') as f:
    crops_data = json.load(f)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        try:
            # Get form data
            ph = float(request.form.get('ph', 0))
            soil_type = request.form.get('soil_type', '')
            moisture = request.form.get('moisture', '')
            print(f"Received input - pH: {ph}, Soil Type: {soil_type}, Moisture: {moisture}")
            
            # Check if exit button was clicked
            if 'exit' in request.form:
                return render_template('goodbye.html')
            
            # Validate pH value
            min_ph = 4.0
            max_ph = 8.5
            if ph < min_ph or ph > max_ph:
                flash(f'Please enter a pH value between {min_ph} and {max_ph}', 'error')
                return render_template('index.html', min_ph=min_ph, max_ph=max_ph)
            
            # Find matching crops
            matching_crops = []
            for crop in crops_data:
                # Check pH range
                if crop['pH_min'] <= ph <= crop['pH_max']:
                    # Check soil type
                    if soil_type.lower() in crop['soil_type'].lower():
                        # Check moisture level
                        if moisture.lower() in crop['moisture_level'].lower():
                            matching_crops.append(crop)
            
            print(f"\nTotal matching crops found: {len(matching_crops)}")
            
            if matching_crops:
                return render_template('index.html', crops=matching_crops, min_ph=min_ph, max_ph=max_ph)
            else:
                flash('No matching crops found for your input. Please try different soil parameters.', 'error')
                return render_template('index.html', min_ph=min_ph, max_ph=max_ph)
        
        except ValueError as e:
            print(f"ValueError: {str(e)}")
            flash('Please enter a valid pH value', 'error')
            return render_template('index.html', min_ph=min_ph, max_ph=max_ph)
        except Exception as e:
            print(f"Error: {str(e)}")
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('index.html', min_ph=min_ph, max_ph=max_ph)
    
    return render_template('index.html', min_ph=4.0, max_ph=8.5)

if __name__ == '__main__':
    app.run(debug=True)

