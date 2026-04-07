"""
Classification Example
======================
Classify iris flowers using multiple algorithms and compare them.

Concepts covered:
- Multi-class classification
- Decision Trees, Random Forest, K-Nearest Neighbors
- Confusion matrix and classification report
- Comparing model accuracy
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# --- 1. Load the Iris dataset ---
print("=" * 60)
print("Classification: Iris Flower Species")
print("=" * 60)

iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"Classes: {list(target_names)}")
print(f"Samples per class: {np.bincount(y)}")

# --- 2. Split data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
print(f"\nTraining samples: {X_train.shape[0]}")
print(f"Test samples: {X_test.shape[0]}")

# --- 3. Train and compare multiple classifiers ---
classifiers = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
}

results = {}
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = {"accuracy": accuracy, "predictions": y_pred, "model": clf}
    print(f"\n--- {name} ---")
    print(f"Accuracy: {accuracy:.4f}")

# --- 4. Detailed report for the best model ---
best_name = max(results, key=lambda k: results[k]["accuracy"])
best_result = results[best_name]
print(f"\n{'=' * 60}")
print(f"Best Model: {best_name} (Accuracy: {best_result['accuracy']:.4f})")
print(f"{'=' * 60}")
print("\nClassification Report:")
print(
    classification_report(
        y_test, best_result["predictions"], target_names=target_names
    )
)

# --- 5. Visualizations ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Confusion matrix for best model
cm = confusion_matrix(y_test, best_result["predictions"])
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=target_names,
    yticklabels=target_names,
    ax=axes[0],
)
axes[0].set_xlabel("Predicted")
axes[0].set_ylabel("Actual")
axes[0].set_title(f"Confusion Matrix ({best_name})")

# Accuracy comparison bar chart
model_names = list(results.keys())
accuracies = [results[n]["accuracy"] for n in model_names]
colors = ["#2196F3", "#4CAF50", "#FF9800"]
bars = axes[1].bar(model_names, accuracies, color=colors)
axes[1].set_ylim(0.8, 1.02)
axes[1].set_ylabel("Accuracy")
axes[1].set_title("Model Comparison")
for bar, acc in zip(bars, accuracies):
    axes[1].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.005,
        f"{acc:.3f}",
        ha="center",
        fontsize=10,
    )

# Feature importance (Random Forest)
rf_model = results["Random Forest"]["model"]
importances = rf_model.feature_importances_
sorted_idx = np.argsort(importances)
short_names = ["Sepal L", "Sepal W", "Petal L", "Petal W"]
axes[2].barh(
    [short_names[i] for i in sorted_idx],
    importances[sorted_idx],
    color="#9C27B0",
)
axes[2].set_xlabel("Importance")
axes[2].set_title("Feature Importance (Random Forest)")

plt.tight_layout()
plt.savefig("examples/output_classification.png", dpi=100)
plt.close()
print("\nPlot saved to examples/output_classification.png")
