from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
import folium

from acmi_parser import parse_acmi

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['tacfile']
        if not file:
            return redirect(request.url)
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return redirect(url_for('analyze', filename=filename))
    return render_template('index.html')

@app.route('/analyze/<filename>')
def analyze(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    events = parse_acmi(path)
    # Summarize statistics per pilot and formation
    summary_by_pilot = events.groupby('pilot').size().reset_index(name='events')
    summary_by_formation = events.groupby('formation').size().reset_index(name='events')

    # Create map with events
    if not events.empty:
        center = [events['lat'].mean(), events['lon'].mean()]
    else:
        center = [0, 0]
    m = folium.Map(location=center, zoom_start=6)
    for idx, row in events.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=row['event']).add_to(m)
    map_html = m._repr_html_()

    return render_template('analysis.html',
                           filename=filename,
                           events=events.to_dict('records'),
                           summary_by_pilot=summary_by_pilot.to_dict('records'),
                           summary_by_formation=summary_by_formation.to_dict('records'),
                           map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
