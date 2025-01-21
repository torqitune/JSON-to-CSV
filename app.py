from flask import Flask, request, jsonify
import json
import csv
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_to_csv():
    try:
        data = request.get_json()  # Get JSON data from the request body
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            output.seek(0)
            return output.getvalue(), 200, {'Content-Type': 'text/csv'}
        else:
            return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
