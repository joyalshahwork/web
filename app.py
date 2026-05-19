
import os
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use("Agg")          
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, jsonify

from src.preprocess import load_data, preprocess
from src.clustering  import find_optimal_k, run_kmeans, apply_pca
from src.visualize   import plot_clusters_2d, plot_segment_profiles, plot_heatmap


app = Flask(__name__)

DATA_PATH = "data/mall_customers.csv"



def fig_to_base64(fig):
    buf = io.BytesIO()             
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight")
    buf.seek(0)                   
    img_bytes = buf.read()
    b64_str = base64.b64encode(img_bytes).decode("utf-8")
    plt.close(fig)                 
    return b64_str


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        n_clusters = int(request.json.get("n_clusters", 5))
        n_clusters = max(2, min(10, n_clusters)) 
        df_raw   = load_data(DATA_PATH)
        X_scaled, scaler, features, df = preprocess(df_raw)
        inertias, silhouettes = [], []
        import numpy as np
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        k_range = range(2, 11)
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(X_scaled, km.labels_))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
        ax1.plot(list(k_range), inertias, "o-", color="#4f46e5")
        ax1.axvline(n_clusters, color="#f59e0b", linestyle="--", label=f"k={n_clusters}")
        ax1.set_title("Elbow Method"); ax1.set_xlabel("k"); ax1.set_ylabel("Inertia")
        ax1.legend()
        ax2.plot(list(k_range), silhouettes, "s-", color="#10b981")
        ax2.axvline(n_clusters, color="#f59e0b", linestyle="--", label=f"k={n_clusters}")
        ax2.set_title("Silhouette Scores"); ax2.set_xlabel("k"); ax2.set_ylabel("Score")
        ax2.legend()
        plt.tight_layout()
        elbow_img = fig_to_base64(fig)
        km_model, labels = run_kmeans(X_scaled, n_clusters=n_clusters)
        df["segment"] = labels + 1    # 1-indexed
        X_pca, _ = apply_pca(X_scaled)
        from src.visualize import PALETTE
        fig_scatter, ax = plt.subplots(figsize=(8, 5))
        for cid in np.unique(labels):
            mask = labels == cid
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                       label=f"Segment {cid+1}",
                       color=PALETTE[cid % len(PALETTE)],
                       alpha=0.7, edgecolors="white", linewidths=0.4, s=60)
        ax.set_title("Customer Segments (PCA 2D)", fontweight="bold")
        ax.set_xlabel("PC 1"); ax.set_ylabel("PC 2"); ax.legend(title="Segment")
        plt.tight_layout()
        scatter_img = fig_to_base64(fig_scatter)

        numeric_cols = ["age", "annual_income_(k$)", "spending_score_(1-100)"]
        available    = [c for c in numeric_cols if c in df.columns]

        import seaborn as sns
        fig_box, axes = plt.subplots(1, len(available), figsize=(5*len(available), 4))
        if len(available) == 1: axes = [axes]
        for ax, col in zip(axes, available):
            sns.boxplot(data=df, x="segment", y=col, hue="segment",
                        palette=PALETTE[:n_clusters], legend=False, ax=ax)
            ax.set_title(col.replace("_"," ").title()); ax.set_xlabel("Segment")
        plt.suptitle("Feature Distribution per Segment", fontweight="bold", y=1.02)
        plt.tight_layout()
        box_img = fig_to_base64(fig_box)

        profile = df.groupby("segment")[available].mean()
        fig_heat, ax = plt.subplots(figsize=(8, 3.5))
        sns.heatmap(profile.T, annot=True, fmt=".1f", cmap="RdYlGn",
                    linewidths=0.5, ax=ax)
        ax.set_title("Segment Mean Feature Heatmap", fontweight="bold")
        plt.tight_layout()
        heat_img = fig_to_base64(fig_heat)

      
        seg_means = df.groupby("segment")[available].mean().round(1)
        seg_counts = df["segment"].value_counts().sort_index()

        RECO = [
            "🎯 VIP loyalty program, premium upsells, exclusive offers",
            "📩 Targeted re-engagement – showcase quality & value",
            "💳 Instalment plans, flash sales, FOMO campaigns",
            "🏷️  Discount-first messaging, bundle deals",
            "📊 Standard retention, seasonal promotions",
        ]

        segments = []
        for seg in seg_means.index:
            row = seg_means.loc[seg]
            segments.append({
                "id":       int(seg),
                "count":    int(seg_counts.get(seg, 0)),
                "age":      row.get("age", "N/A"),
                "income":   row.get("annual_income_(k$)", "N/A"),
                "spending": row.get("spending_score_(1-100)", "N/A"),
                "reco":     RECO[(seg - 1) % len(RECO)],
            })


        return jsonify({
            "success":    True,
            "n_clusters": n_clusters,
            "elbow_img":  elbow_img,
            "scatter_img":scatter_img,
            "box_img":    box_img,
            "heat_img":   heat_img,
            "segments":   segments,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
