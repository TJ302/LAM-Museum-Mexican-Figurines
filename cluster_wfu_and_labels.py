#!/usr/bin/env python3
"""
cluster_wfu_and_labels.py
Runs KMeans clustering on:
- wfudataset.txt (feature vectors for ALL images)
- labels.txt (JSONL of human-labeled regions + vectors)

Outputs:
- clusters.txt
- label_region_distribution.png
- cluster_region_probabilities.json
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Load labeled data (JSONL)
# ---------------------------------------------------------------------

def load_labeled_vectors(labels_path: Path):
    labeled_vectors = {}
    regions = []

    with labels_path.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            image_id = obj["imageId"]
            vector = np.array(obj["vector"], dtype=float)
            region = obj["region"]

            labeled_vectors[image_id] = vector
            regions.append(region)

    return labeled_vectors, regions


# ---------------------------------------------------------------------
# Load WFU dataset vectors from txt
# ---------------------------------------------------------------------

def load_wfu_vectors(path: Path):
    data = np.loadtxt(path, delimiter=",")
    return data


# ---------------------------------------------------------------------
# Pie chart for cluster region distributions
# ---------------------------------------------------------------------

def plot_cluster_region_pies(cluster_region_counts, output_png):
    labels = []
    sizes = []

    for region, count in Counter(
        r for d in cluster_region_counts.values() for r in d
    ).items():
        labels.append(region)
        sizes.append(count)

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Overall Region Distribution")
    plt.savefig(output_png)
    plt.close()


# ---------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wfu", required=True, type=str)
    parser.add_argument("--labels", required=True, type=str)
    parser.add_argument("--output", required=True, type=str)
    parser.add_argument("--clusters", type=int, default=3)
    args = parser.parse_args()

    wfu_path = Path(args.wfu)
    labels_path = Path(args.labels)
    output_png = Path(args.output)

    # Load labeled data
    labeled_vectors, labeled_regions = load_labeled_vectors(labels_path)
    if len(labeled_vectors) == 0:
        print("ERROR: No labeled data found. Please save some labels first.")
        return 1

    X = np.array(list(labeled_vectors.values()))

    # KMeans clustering
    model = KMeans(n_clusters=args.clusters, random_state=42)
    cluster_assignments = model.fit_predict(X)

    # Count regions in each cluster
    cluster_region_counts = defaultdict(Counter)
    for region, cluster in zip(labeled_regions, cluster_assignments):
        cluster_region_counts[int(cluster)][region] += 1

    # Save cluster-region probabilities
    cluster_probabilities = {}
    for cluster, reg_counts in cluster_region_counts.items():
        total = sum(reg_counts.values())
        for r, c in reg_counts.items():
            pct = 100.0 * c / total if total > 0 else 0.0
            print(f"    {r}: {c} ({pct:.1f}%)")

    # 6. Plot region distribution as a pie chart (overall labeled data)
    plot_cluster_region_pies(cluster_region_counts, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
