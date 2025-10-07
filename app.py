from flask import Flask, render_template
import pandas as pd
import folium

app = Flask(__name__)

@app.route('/')
def home():
    # Load the dataset
    data = pd.read_csv('bus_routes.csv')

    # Some quick calculations
    total_buses = len(data)
    avg_students = round(data['Avg_Students'].mean(), 2)
    earliest_bus = data.loc[data['Departure_Time'].idxmin()]

    # Create a map centered roughly on the campus
    m = folium.Map(location=[13.1147, 80.0956], zoom_start=12)

    # Plot each route on the map
    for _, row in data.iterrows():
        start = [row['Start_Latitude'], row['Start_Longitude']]
        end = [row['End_Latitude'], row['End_Longitude']]

        folium.Marker(
            start, popup=f"Bus {row['Bus_No']} ({row['Start_Stop']}) - {row['Departure_Time']}", 
            icon=folium.Icon(color='blue', icon='bus', prefix='fa')
        ).add_to(m)

        folium.Marker(
            end, popup=f"{row['End_Stop']} (Arrives: {row['Arrival_Time']})", 
            icon=folium.Icon(color='green')
        ).add_to(m)

        folium.PolyLine([start, end], color='red', weight=2.5, opacity=1).add_to(m)

    # Save map as HTML file
    m.save('templates/map.html')

    # Pass data to the main page
    return render_template(
        'index.html',
        tables=data.to_html(classes='data', index=False),
        total_buses=total_buses,
        avg_students=avg_students,
        earliest_stop=earliest_bus['Start_Stop'],
        earliest_time=earliest_bus['Departure_Time']
    )

@app.route('/map')
def map_page():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)

