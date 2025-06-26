from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = os.path.join('artifacts', 'model.pkl')
PREPROCESSOR_PATH = os.path.join('artifacts', 'preprocessor.pkl')

# Load model and preprocessor
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
with open(PREPROCESSOR_PATH, 'rb') as f:
    preprocessor = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            carat = float(request.form['carat'])
            depth = float(request.form['depth'])
            table = float(request.form['table'])
            x = float(request.form['x'])
            y = float(request.form['y'])
            z = float(request.form['z'])
            cut = request.form['cut']
            color = request.form['color']
            clarity = request.form['clarity']
            data = np.array([[carat, cut, color, clarity, depth, table, x, y, z]])
            data_df = preprocessor.transformers_[0][1].named_steps['imputer']._validate_data(data[:, [0, 4, 5, 6, 7, 8]].astype(float))
            data_processed = preprocessor.transform(data)
            prediction = model.predict(data_processed)
            result = round(prediction[0], 2)
            return render_template('result.html', prediction=result)
        except Exception as e:
            return render_template('result.html', prediction=f"Error: {e}")
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True) 