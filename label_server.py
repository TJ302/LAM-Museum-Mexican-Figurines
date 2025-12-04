from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import json
import sys
import subprocess

app = Flask(__name__)

# Allow Vite dev server (localhost:5173) to talk to this
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

# labels.txt will live next to label_server.py
LABELS_FILE = Path(__file__).with_name("labels.txt")


@app.post("/api/save-labels")
def save_labels():
    print(">>> /api/save-labels hit", file=sys.stderr)

    data = request.get_json(silent=True) or {}
    image_id = data.get("imageId")
    region = data.get("region")
    vector = data.get("vector")

    print("   payload:", data, file=sys.stderr)

    if image_id is None or vector is None:
        print("   ERROR: missing imageId or vector", file=sys.stderr)
        return jsonify({"error": "imageId and vector are required"}), 400

    record = {
        "imageId": image_id,
        "region": region,
        "vector": vector,
    }


    

    # Append one JSON record per line
    with LABELS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print("   appended to", LABELS_FILE, file=sys.stderr)
    return jsonify({"status": "ok"})



@app.route("/api/run-cluster", methods=["POST"])
def run_cluster():
    try:
        # Runs your Python script
        result = subprocess.run(
            ["py", "cluster_wfu_and_labels.py"],
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({"success": True, "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": e.stderr}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
