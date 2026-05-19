import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

def find_optimal_k(X_scaled, k_range=range(2, 11), save_path=None):
    """Elbow method + silhouette scores to pick best k."""
    inertias, silhouettes = [], []

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, km.labels_))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(list(k_range), inertias, "bo-")
    ax1.set_title("Elbow Method")
    ax1.set_xlabel("Number of clusters (k)")
    ax1.set_ylabel("Inertia")

    ax2.plot(list(k_range), silhouettes, "gs-")
    ax2.set_title("Silhouette Scores")
    ax2.set_xlabel("Number of clusters (k)")
    ax2.set_ylabel("Silhouette Score")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    return inertias, silhouettes


def run_kmeans(X_scaled, n_clusters=5):
    """Fit final K-Means model."""
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    print(f"Inertia: {km.inertia_:.2f}")
    print(f"Silhouette Score: {silhouette_score(X_scaled, labels):.3f}")
    return km, labels


def apply_pca(X_scaled, n_components=2):
    """Reduce to 2D for visualization."""
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
    return X_pca, pca