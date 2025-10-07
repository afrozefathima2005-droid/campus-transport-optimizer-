from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # Load the dataset
    data = pd.read_csv('bus_routes.csv')

    # Some simple calculations
    total_buses = len(data)
    avg_students = round(data['Avg_Students'].mean(), 2)
    earliest_bus = data.loc[data['Departure_Time'].idxmin()]

    # Pass data to HTML
    return render_template(
        'index.html',
        tables=data.to_html(classes='data', index=False),
        total_buses=total_buses,
        avg_students=avg_students,
        earliest_stop=earliest_bus['Start_Stop'],
        earliest_time=earliest_bus['Departure_Time']
    )

if __name__ == '__main__':
    app.run(debug=True)
