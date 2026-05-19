import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

PALETTE = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]

def plot_clusters_2d(X_pca, labels, save_path=None):
    """Scatter plot of PCA-reduced clusters."""
    fig, ax = plt.subplots(figsize=(9, 6))
    for cluster_id in np.unique(labels):
        mask = labels == cluster_id
        ax.scatter(
            X_pca[mask, 0], X_pca[mask, 1],
            label=f"Segment {cluster_id + 1}",
            color=PALETTE[cluster_id % len(PALETTE)],
            alpha=0.7, edgecolors="white", linewidths=0.4, s=60
        )
    ax.set_title("Customer Segments (PCA 2D)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.legend(title="Segment")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_segment_profiles(df, save_path=None):
    """Box plots: key features per segment."""
    numeric_cols = ["age", "annual_income_(k$)", "spending_score_(1-100)"]
    available = [c for c in numeric_cols if c in df.columns]

    fig, axes = plt.subplots(1, len(available), figsize=(5 * len(available), 5))
    if len(available) == 1:
        axes = [axes]

    for ax, col in zip(axes, available):
        sns.boxplot(data=df, x="segment", y=col, palette=PALETTE, ax=ax)
        ax.set_title(col.replace("_", " ").title())
        ax.set_xlabel("Segment")

    plt.suptitle("Feature Distribution per Segment", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_heatmap(df, save_path=None):
    """Heatmap of mean features per segment."""
    numeric_cols = ["age", "annual_income_(k$)", "spending_score_(1-100)"]
    available = [c for c in numeric_cols if c in df.columns]
    profile = df.groupby("segment")[available].mean()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(profile.T, annot=True, fmt=".1f", cmap="RdYlGn",
                linewidths=0.5, ax=ax)
    ax.set_title("Segment Mean Feature Heatmap", fontsize=13, fontweight="bold")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()