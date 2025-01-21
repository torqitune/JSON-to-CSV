from flask import Flask, request, jsonify, send_file
import json
import csv
import os
import uuid

app = Flask(__name__)

# Directory to store temporary CSV files
TEMP_DIR = "temp_csvs"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/convert', methods=['POST'])
def convert_to_csv():
    try:
        data = request.get_json()  # Get JSON data from the request body
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Create a unique file name
            file_id = str(uuid.uuid4())
            file_path = os.path.join(TEMP_DIR, f"{file_id}.csv")
            
            # Write data to a CSV file
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            # Generate download link
            download_url = f"{request.host_url}download/{file_id}"
            return jsonify({"message": "CSV generated", "download_url": download_url}), 200
        else:
            return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<file_id>', methods=['GET'])
def download_csv(file_id):
    try:
        file_path = os.path.join(TEMP_DIR, f"{file_id}.csv")
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
