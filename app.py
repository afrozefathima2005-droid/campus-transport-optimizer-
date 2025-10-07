from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    data = pd.read_csv('stops.csv')
    return render_template('index.html', tables=data.to_html(classes='data', header="true"))

if __name__ == '__main__':
    app.run(debug=True)
