from flask import Flask, render_template
import os



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'test.jpg')
    return render_template("index.html", captured_photo = full_filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')

    