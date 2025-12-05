#!/usr/bin/env python3
"""
label_server.py
Backend server for LAM Museum Mexican Figurines project.

Provides:
- /api/save-labels       ← save labeled image vectors
- /api/run-cluster       ← runs clustering script
- /api/cluster-results   ← returns clustering output & probabilities
- /download/clusters     ← download clusters.txt
- /static/...            ← serve PNG + any static files
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from flask import Flask, jsonify, request, send_file, send_from_directory

# ---------------------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent

LABELS_PATH = ROOT / "labels.txt"
WFU_PATH = ROOT / "wfudataset.txt"
CLUSTER_SCRIPT = ROOT / "cluster_wfu_and_labels.py"

PNG_PATH = ROOT / "label_region_distribution.png"
CLUSTERS_TXT = ROOT / "clusters.txt"
PROBS_JSON = ROOT / "cluster_region_probabilities.json"

app = Flask(__name__)


# ---------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


# ---------------------------------------------------------------------
# SAVE LABELS
# ---------------------------------------------------------------------

@app.route("/api/save-labels", methods=["POST", "OPTIONS"])
def save_labels():
    if request.method == "OPTIONS":
        return ("", 204)

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    image_id = data.get("imageId")
    region = data.get("region")
    vector = data.get("vector")

    if not image_id or not region or not isinstance(vector, list):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    try:
        vector = [float(v) for v in vector]
    except Exception:
        return jsonify({"success": False, "error": "Vector must contain numbers"}), 400

    entry = {"imageId": image_id, "region": region, "vector": vector}

    try:
        with LABELS_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        return jsonify({"success": False, "error": f"Cannot write to labels.txt: {e}"}), 500

    return jsonify({"success": True})


# ---------------------------------------------------------------------
# RUN CLUSTERING SCRIPT
# ---------------------------------------------------------------------

@app.route("/api/run-cluster", methods=["POST", "OPTIONS"])
def run_cluster():
    if request.method == "OPTIONS":
        return ("", 204)

    # Check all inputs exist
    if not CLUSTER_SCRIPT.exists():
        return jsonify({"success": False, "error": "cluster_wfu_and_labels.py missing"}), 500
    if not WFU_PATH.exists():
        return jsonify({"success": False, "error": "wfudataset.txt missing"}), 500
    if not LABELS_PATH.exists():
        return jsonify({"success": False, "error": "labels.txt missing"}), 400

    cmd = [
        "python",
        str(CLUSTER_SCRIPT),
        "--wfu", str(WFU_PATH),
        "--labels", str(LABELS_PATH),
        "--output", str(PNG_PATH),
    ]

    try:
        process = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to run script: {e}"}), 500

    stdout = process.stdout
    stderr = process.stderr

    # Print for debugging
    print("\n======== CLUSTER SCRIPT OUTPUT ========")
    print(stdout)
    print("--------------- ERROR -----------------")
    print(stderr)
    print("=======================================\n")

    if process.returncode != 0:
        return jsonify({
            "success": False,
            "error": "Clustering script exited with non-zero status.",
            "stdout": stdout,
            "stderr": stderr
        }), 500

    return jsonify({
        "success": True,
        "stdout": stdout,
        "stderr": stderr
    })


# ---------------------------------------------------------------------
# GET CLUSTER RESULTS FOR REPORT PAGE
# ---------------------------------------------------------------------

@app.route("/api/cluster-results", methods=["GET"])
def cluster_results():

    if not CLUSTERS_TXT.exists():
        return jsonify({"success": False, "error": "clusters.txt not found"}), 404

    # Parse clusters.txt
    rows = []
    try:
        with CLUSTERS_TXT.open("r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) != 3:
                    continue
                image_id, region, cluster = parts
                try:
                    cluster = int(cluster)
                except:
                    pass
                rows.append({
                    "imageId": image_id,
                    "region": region,
                    "cluster": cluster
                })
    except Exception as e:
        return jsonify({"success": False, "error": f"Error reading clusters.txt: {e}"}), 500

    # Read probabilities JSON if exists
    probabilities = {}
    if PROBS_JSON.exists():
        try:
            probabilities = json.loads(PROBS_JSON.read_text())
        except Exception as e:
            print(f"[WARN] Failed to load probabilities JSON: {e}")

    return jsonify({
        "success": True,
        "rows": rows,
        "probabilities": probabilities,
        "pngUrl": "/static/label_region_distribution.png",
        "downloadUrl": "/download/clusters"
    })


# ---------------------------------------------------------------------
# FILE DOWNLOAD
# ---------------------------------------------------------------------

@app.route("/download/clusters", methods=["GET"])
def download_clusters():
    if not CLUSTERS_TXT.exists():
        return "clusters.txt not found", 404

    return send_file(
        str(CLUSTERS_TXT),
        mimetype="text/plain",
        as_attachment=True,
        download_name="clustering_results.txt"
    )


# ---------------------------------------------------------------------
# STATIC FILES (PNG)
# ---------------------------------------------------------------------

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(str(ROOT), filename)


# ---------------------------------------------------------------------
# HEALTHCHECK
# ---------------------------------------------------------------------

@app.route("/")
def health():
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
