from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = "data.csv"

# Load or initialize CSV
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["text", "context", "sentiment", "risk"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_text", methods=["GET"])
def get_text():
    df = load_data()
    df_unlabeled = df[df["context"].isnull()]
    if not df_unlabeled.empty:
        row = df_unlabeled.iloc[0]
        return jsonify({
            "index": int(row.name),
            "text": row["text"]
        })
    else:
        return jsonify({"message": "All rows have been labeled."})

@app.route("/submit_label", methods=["POST"])
def submit_label():
    index = int(request.form.get("index"))
    context = request.form.get("context")
    sentiment = request.form.get("sentiment")
    risk = request.form.get("risk")

    df = load_data()
    if 0 <= index < len(df):
        df.at[index, "context"] = context
        df.at[index, "sentiment"] = sentiment
        df.at[index, "risk"] = risk
        save_data(df)
        return jsonify({"message": "Label submitted successfully"})
    else:
        return jsonify({"message": "Invalid index"}), 404

# Run app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
