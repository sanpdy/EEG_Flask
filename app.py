from flask import Flask, render_template, jsonify, send_file
import pandas as pd
import random
import io
from PIL import Image
import numpy as np
from record import Record  # Import the Record class

app = Flask(__name__)

# Load the dataset
train_df = pd.read_csv('../samples/mnist_train.csv')
test_df = pd.read_csv('../samples/mnist_test.csv')
data = pd.concat([train_df, test_df], ignore_index=True)

# Initialize state
random_indices = random.sample(range(len(data)), 10)
current_index = 0

# Initialize the Record object
record_duration_s = 10
app_client_id = 'fpCi6nTQcc4Cts2sIAsXNL1xkXOGmIorihpdNbep'
app_client_secret = '7KBmJhfKAgHvWm9FfMZLaHv3x0EfRERToaRuL3cvJd3JL93ljIZlqD6ndM9UYcT181Okb49m8GRA0oI1Ntanw9VfXC7TqI3440l3aUYNDrJUdw2iduvWQzSbyLu5YAc0'
record = Record(app_client_id, app_client_secret)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording')
def start_recording():
    record.start(record_duration_s=record_duration_s)
    return jsonify(success=True)

@app.route('/stop_recording')
def stop_recording():
    record.stop_record()
    return jsonify(success=True)

@app.route('/previous_image')
def previous_image():
    global current_index
    current_index = (current_index - 1) % len(random_indices)
    return jsonify(success=True)

@app.route('/next_image')
def next_image():
    global current_index
    current_index = (current_index + 1) % len(random_indices)
    return jsonify(success=True)

@app.route('/current_image')
def current_image():
    global current_index
    row = data.iloc[random_indices[current_index]]
    pixels = row[1:].values.reshape(28, 28).astype(np.uint8)
    image = Image.fromarray(pixels, 'L')
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
