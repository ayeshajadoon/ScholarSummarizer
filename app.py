from flask import Flask, render_template, request, jsonify
from model import summarize_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.form['text']
    summary = summarize_text(data)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run()
