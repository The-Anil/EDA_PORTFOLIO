from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json['html']
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(data)
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
