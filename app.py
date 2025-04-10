from flask import Flask, request, jsonify, render_template
import csv
import os

app = Flask(__name__)

CSV_FILE = "data/sample.csv"

# Load the CSV file into memory
def load_csv():
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

data = load_csv()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_row")
def get_row():
    for i, row in enumerate(data):
        if not row.get("context"):
            return jsonify({"index": i, "text": row["text"]})
    return jsonify({"message": "All done! Great job 🎉"})

@app.route("/submit_label", methods=["POST"])
def submit_label():
    req_data = request.get_json()
    index = req_data.get("index")
    context = req_data.get("context")

    if index is None or context is None:
        return jsonify({"error": "Missing index or context"}), 400

    data[int(index)]["context"] = context

    # Save back to CSV
    fieldnames = data[0].keys()
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return jsonify({"message": "Context added successfully!"})

if __name__ == "__main__":
    app.run(debug=True)