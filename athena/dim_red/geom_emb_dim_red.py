#!/usr/bin/env python
# coding: utf-8
# 
# # Large scale dimensionality reduction
# 
# Piotr Urbańczyk,
# Piotr Van-Selow

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP
from pacmap import PaCMAP
from trimap import TRIMAP

# Define output directory
OUTPUT_DIR = "./dim_red/output_2nodes_run1"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the dataset
def load_data(file_path):
    print(f"Loading data from {file_path}...")
    X_loaded = np.load(file_path, allow_pickle=True)
    print(f"Data shape: {X_loaded.shape}")
    return X_loaded

# Save results to CSV
def save_results_to_csv(results, csv_path):
    print(f"Saving results to {csv_path}...")
    rows = []
    for name, result in results.items():
        rows.append({"Reducer": name, "Time (seconds)": result["time"]})
    df = pd.DataFrame(rows)
    if os.path.exists(csv_path):
        # Append to existing CSV
        existing_df = pd.read_csv(csv_path)
        df = pd.concat([existing_df, df]).drop_duplicates(subset="Reducer")
    df.to_csv(csv_path, index=False)

# Save a plot to the output directory
def save_plot(data, title, output_path):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data[:, 0], data[:, 1], s=5, alpha=0.7)
    ax.set_xlabel("Component 1")
    ax.set_ylabel("Component 2")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    print(f"Saved plot: {output_path}")

# Check if results/plots already exist
def check_existing_output(name):
    plot_path = os.path.join(OUTPUT_DIR, f"{name}_reduction_plot.png")
    csv_path = os.path.join(OUTPUT_DIR, "results.csv")
    return os.path.exists(plot_path), csv_path

# Run and store the results of dimensionality reduction
def run_experiments(X):
    reducers = {
        "PCA": PCA(n_components=2),
        "TriMap": TRIMAP(n_dims=2),
        "PaCMAP": PaCMAP(n_components=2, n_neighbors=10, MN_ratio=0.5, FP_ratio=2.0),
        "t-SNE": TSNE(n_components=2, perplexity=50, n_iter=500),
        "UMAP": UMAP(n_components=2),
    }

    results = {}
    print("Starting dimensionality reduction experiments...")
    for name, reducer in reducers.items():
        plot_exists, csv_path = check_existing_output(name)
        if plot_exists:
            print(f"Skipping {name}: plot already exists.")
            continue

        print(f"Running {name}...")
        start_time = time.time()
        X_reduced = reducer.fit_transform(X)
        elapsed_time = time.time() - start_time
        results[name] = {"data": X_reduced, "time": elapsed_time}
        print(f"{name} completed in {elapsed_time:.2f} seconds.")

        # Save plot
        plot_path = os.path.join(OUTPUT_DIR, f"{name}_reduction_plot.png")
        save_plot(X_reduced, f"{name} Reduction", plot_path)

        # Save results to CSV
        save_results_to_csv(results, csv_path)

    return results

# Plot a single result
def plot_single_result(name, result):
    plot_path = os.path.join(OUTPUT_DIR, f"{name}_reduction_plot.png")
    save_plot(result["data"], f"{name} Reduction", plot_path)

# Pairwise relationships plot
def plot_pairwise_features(X):
    pairplot_path = os.path.join(OUTPUT_DIR, "pairwise_features_plot.png")
    
    if os.path.exists(pairplot_path):
        print(f"Pairwise features plot already exists: {pairplot_path}. Skipping...")
        return
    
    print("Generating pairwise features plot...")
    sampled_features = np.random.choice(X.shape[1], size=5, replace=False)
    df_sampled = pd.DataFrame(X[:, sampled_features], columns=[f"Feature {i}" for i in range(5)])
    sns.pairplot(df_sampled)
    plt.tight_layout()
    plt.savefig(pairplot_path)
    plt.close()
    print(f"Saved pairwise features plot: {pairplot_path}")

# Main script
if __name__ == "__main__":
    # File path
    file_path = "/net/pr2/projects/plgrid/plgglscclass/geometricus_embeddings/X_concatenated_all_dims.npy"

    # Load data
    X_loaded = load_data(file_path)

    # Plot pairwise relationships
    plot_pairwise_features(X_loaded)

    # Run experiments
    results = run_experiments(X_loaded)
