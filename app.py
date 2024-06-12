from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

downloads = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"status": "success", "filename": file.filename})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    client_info = {
        "ip": request.remote_addr,
        "user_agent": request.user_agent.string,
        "timestamp": datetime.now().isoformat()
    }
    downloads.append(client_info)
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(downloads)

@app.route('/stats_page')
def stats_page():
    return render_template('stats.html', downloads=downloads)

if __name__ == '__main__':
    app.run(debug=True)
