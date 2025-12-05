#!/usr/bin/env python3
"""
cluster_wfu_and_labels.py

1. Load feature vectors from wfudataset.txt (JSON lines).
   - Each line should have at least: {"imageId": ..., "vector": [...]}
   - There may be MULTIPLE vectors per imageId -> we AVERAGE them.

2. Fit a 3-cluster KMeans model on the averaged WFU feature vectors.

3. Load feature vectors from label.txt (JSON lines).
   - Each line should have at least: {"imageId": ..., "region": "...", "vector": [...]}
   - Again, there may be MULTIPLE vectors per imageId -> we AVERAGE them.
   - Region is taken from the JSON "region" field.

4. Use the trained KMeans model to assign each averaged label vector to a cluster.

5. Compute and save a pie chart showing the distribution of labeled data by region.

Usage (from repo root):

    python cluster_wfu_and_labels.py \
        --wfu wfudataset.txt \
        --labels label.txt \
        --output label_region_distribution.png

Dependencies:

    pip install numpy scikit-learn matplotlib
"""

import argparse
import json
from collections import defaultdict, Counter
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def load_jsonl_vectors_grouped(path, require_region=False):
    """
    Load a JSONL file where each line is an object that includes:

        imageId: str
        vector: list of numbers
        (optionally) region: str

    Returns:
        avg_vectors: dict imageId -> np.array averaged vector
        regions: dict imageId -> region (or None)
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    vectors_by_id = defaultdict(list)
    region_by_id = {}

    with path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"[WARN] Skipping invalid JSON on line {line_num}: {e}")
                continue

            image_id = obj.get("imageId") or obj.get("image_id") or obj.get("id")
            vector = obj.get("vector")

            if image_id is None or vector is None:
                print(f"[WARN] Skipping line {line_num}: missing imageId or vector")
                continue

            # Convert vector to numpy float array
            try:
                vec_arr = np.array(vector, dtype=float)
            except Exception as e:
                print(
                    f"[WARN] Could not convert vector to float on line {line_num}: {e}"
                )
                continue

            vectors_by_id[image_id].append(vec_arr)

            # Region handling (for label.txt)
            if "region" in obj:
                region = obj["region"]
                if image_id in region_by_id and region_by_id[image_id] != region:
                    print(
                        f"[WARN] Conflicting regions for {image_id}: "
                        f"{region_by_id[image_id]!r} vs {region!r}"
                    )
                region_by_id[image_id] = region

    if require_region:
        # Enforce region presence if needed
        missing = [
            img_id for img_id in vectors_by_id.keys() if img_id not in region_by_id
        ]
        if missing:
            print(
                f"[WARN] {len(missing)} imageIds in {path} had no 'region' field. "
                f"Regions will be set to 'Unknown' for those."
            )
            for img_id in missing:
                region_by_id[img_id] = "Unknown"

    # Average vectors per imageId
    avg_vectors = {}
    for image_id, vec_list in vectors_by_id.items():
        stacked = np.vstack(vec_list)  # shape: (num_vectors_for_image, dim)
        avg = stacked.mean(axis=0)
        avg_vectors[image_id] = avg

    return avg_vectors, region_by_id


def train_kmeans_on_wfu(wfu_vectors, n_clusters=3, random_state=42):
    """
    Train a KMeans clustering model on the given averaged WFU feature vectors.

    Args:
        wfu_vectors: dict imageId -> np.array vector
        n_clusters: int, default 3
        random_state: int

    Returns:
        model: trained KMeans instance
        X_train: np.ndarray of shape (n_samples, n_features)
        image_ids: list of imageIds corresponding to rows of X_train
    """
    if not wfu_vectors:
        raise ValueError("No WFU vectors found to train on.")

    image_ids = sorted(wfu_vectors.keys())
    X_train = np.vstack([wfu_vectors[img_id] for img_id in image_ids])

    print(f"[INFO] Training KMeans with k={n_clusters} on {X_train.shape[0]} instances")
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10,
    )
    kmeans.fit(X_train)
    return kmeans, X_train, image_ids


def apply_model_to_labels(model, wfu_dim, label_vectors, label_regions):
    """
    Apply trained clustering model to label vectors.

    Args:
        model: trained KMeans
        wfu_dim: dimension of WFU feature vectors
        label_vectors: dict imageId -> np.array vector
        label_regions: dict imageId -> region string

    Returns:
        regions_used: list of region strings for each used label instance
        cluster_assignments: list of cluster indices for same
    """
    regions_used = []
    cluster_assignments = []

    for image_id, vec in label_vectors.items():
        if vec.shape[0] != wfu_dim:
            print(
                f"[WARN] Skipping label {image_id}: vector dim {vec.shape[0]} "
                f"does not match WFU dim {wfu_dim}"
            )
            continue

        region = label_regions.get(image_id, "Unknown")
        # Reshape to (1, -1) for prediction
        cluster = model.predict(vec.reshape(1, -1))[0]

        regions_used.append(region)
        cluster_assignments.append(cluster)

    print(
        f"[INFO] Applied model to {len(regions_used)} label instances "
        f"(dimension {wfu_dim})."
    )
    return regions_used, cluster_assignments


def plot_cluster_region_pies(cluster_region_counts, output_path):
    """
    Create and save pie charts showing region distribution for each cluster.

    Args:
        cluster_region_counts: dict[int, Counter] mapping cluster_id -> Counter(region -> count)
        output_path: path to save PNG
    """
    if not cluster_region_counts:
        print("[WARN] No cluster-region data to plot; pies will not be created.")
        return

    # Sort clusters by id so plots are in order 0,1,2,...
    sorted_clusters = sorted(cluster_region_counts.keys())
    num_clusters = len(sorted_clusters)

    # Create one subplot per cluster
    fig, axes = plt.subplots(
        1,
        num_clusters,
        figsize=(5 * num_clusters, 5),
        squeeze=False,
    )
    axes = axes[0]  # single row

    for ax_idx, cluster_id in enumerate(sorted_clusters):
        ax = axes[ax_idx]
        counts = cluster_region_counts[cluster_id]

        labels = list(counts.keys())
        sizes = [counts[r] for r in labels]

        if not sizes or sum(sizes) == 0:
            ax.text(
                0.5,
                0.5,
                "No data",
                ha="center",
                va="center",
                fontsize=10,
                color="white",
            )
            ax.set_axis_off()
            continue

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.axis("equal")
        ax.set_title(f"Cluster {cluster_id}")

    fig.suptitle("Region distribution per cluster (labels)", fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    output_path = Path(output_path)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[INFO] Saved per-cluster region pie charts to {output_path}")



def main():
    parser = argparse.ArgumentParser(
        description=(
            "Train a 3-cluster KMeans model on WFU feature vectors in wfudataset.txt, "
            "then apply it to feature vectors in label.txt and plot region distribution."
        )
    )
    parser.add_argument(
        "--wfu",
        type=str,
        default="wfudataset.txt",
        help="Path to WFU feature dataset (JSONL). Default: wfudataset.txt",
    )
    parser.add_argument(
        "--labels",
        type=str,
        default="labels.txt",
        help="Path to label dataset (JSONL). Default: label.txt",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="label_region_distribution.png",
        help="Output path for the region distribution pie chart (PNG).",
    )
    parser.add_argument(
        "--clusters",
        type=int,
        default=3,
        help="Number of KMeans clusters (default: 3).",
    )
    args = parser.parse_args()

    # 1. Load WFU dataset
    print(f"[INFO] Loading WFU features from {args.wfu}")
    wfu_vectors, _ = load_jsonl_vectors_grouped(args.wfu, require_region=False)
    print(f"[INFO] Aggregated {len(wfu_vectors)} unique WFU imageIds.")

    # 2. Train KMeans on WFU
    kmeans, X_train, wfu_image_ids = train_kmeans_on_wfu(
        wfu_vectors, n_clusters=args.clusters
    )
    wfu_dim = X_train.shape[1]
    print(f"[INFO] Feature dimension (WFU): {wfu_dim}")

    # 3. Load labels dataset
    print(f"[INFO] Loading label features from {args.labels}")
    label_vectors, label_regions = load_jsonl_vectors_grouped(
        args.labels, require_region=True
    )
    print(f"[INFO] Aggregated {len(label_vectors)} unique label imageIds.")

    # 4. Apply model to label data
    regions_used, cluster_assignments = apply_model_to_labels(
        kmeans, wfu_dim, label_vectors, label_regions
    )

    # 5. Print simple cluster x region stats (optional, for inspection)
    print("[INFO] Cluster x Region composition (labels):")
    cluster_region_counts = defaultdict(Counter)
    for region, cluster in zip(regions_used, cluster_assignments):
        cluster_region_counts[cluster][region] += 1

    for cluster, reg_counts in cluster_region_counts.items():
        print(f"  Cluster {cluster}:")
        total = sum(reg_counts.values())
        for r, c in reg_counts.items():
            pct = 100.0 * c / total if total > 0 else 0.0
            print(f"    {r}: {c} ({pct:.1f}%)")
    
    clusters_out = Path("clusters.txt")
    with clusters_out.open("w", encoding="utf-8") as f:
        for image_id, region, cluster in zip(label_vectors.keys(), regions_used, cluster_assignments):
            f.write(f"{image_id}\t{region}\t{cluster}\n")

    print(f"[INFO] Saved cluster assignments to {clusters_out}")
    
    # 6. Plot region distribution as a pie chart (overall labeled data)
    plot_cluster_region_pies(cluster_region_counts, args.output)


if __name__ == "__main__":
    main()
