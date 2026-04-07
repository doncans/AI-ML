"""
Clustering Example
==================
Group customers into segments using K-Means clustering.

Concepts covered:
- Unsupervised learning (no labels needed)
- K-Means algorithm
- Elbow method to find optimal number of clusters
- Cluster visualization
- Feature scaling with StandardScaler
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# --- 1. Generate synthetic customer data ---
print("=" * 60)
print("Clustering: Customer Segmentation with K-Means")
print("=" * 60)

np.random.seed(42)
X, y_true = make_blobs(
    n_samples=300,
    centers=4,
    cluster_std=[1.0, 1.5, 0.8, 1.2],
    random_state=42,
)

# Rename axes for a realistic scenario
print(f"\nGenerated {X.shape[0]} synthetic customer data points")
print(f"Features: Annual Spending Score, Loyalty Score")
print(f"True number of clusters: 4")

# --- 2. Scale the features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"\nFeatures scaled to zero mean and unit variance")

# --- 3. Elbow method to find optimal K ---
inertias = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    if k <= 6:
        print(f"  K={k}: Inertia = {km.inertia_:.1f}")

# --- 4. Fit K-Means with optimal K ---
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

print(f"\nOptimal K = {optimal_k}")
print(f"Cluster sizes: {np.bincount(cluster_labels)}")

# --- 5. Analyze clusters ---
print("\nCluster Centers (scaled):")
for i, center in enumerate(kmeans.cluster_centers_):
    print(f"  Cluster {i}: Spending = {center[0]:+.2f}, Loyalty = {center[1]:+.2f}")

# --- 6. Visualizations ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Original data (unlabeled)
axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], s=20, alpha=0.6, color="gray")
axes[0].set_xlabel("Spending Score (scaled)")
axes[0].set_ylabel("Loyalty Score (scaled)")
axes[0].set_title("Raw Data (Unlabeled)")

# Elbow plot
axes[1].plot(k_range, inertias, "bo-", linewidth=2)
axes[1].axvline(x=optimal_k, color="red", linestyle="--", label=f"K={optimal_k}")
axes[1].set_xlabel("Number of Clusters (K)")
axes[1].set_ylabel("Inertia")
axes[1].set_title("Elbow Method")
axes[1].legend()

# Clustered data
colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]
for i in range(optimal_k):
    mask = cluster_labels == i
    axes[2].scatter(
        X_scaled[mask, 0],
        X_scaled[mask, 1],
        s=20,
        alpha=0.6,
        color=colors[i],
        label=f"Cluster {i}",
    )
axes[2].scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    s=200,
    c="black",
    marker="X",
    linewidths=2,
    label="Centroids",
)
axes[2].set_xlabel("Spending Score (scaled)")
axes[2].set_ylabel("Loyalty Score (scaled)")
axes[2].set_title("K-Means Clustering Result")
axes[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig("examples/output_clustering.png", dpi=100)
plt.close()
print("\nPlot saved to examples/output_clustering.png")
