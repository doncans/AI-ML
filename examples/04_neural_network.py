"""
Neural Network Example
======================
Build a simple neural network to classify handwritten digits (0-9).

Concepts covered:
- Multi-layer Perceptron (MLP) classifier
- Image classification with pixel features
- Training curves and convergence
- Visualizing predictions on real digit images
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# --- 1. Load the digits dataset ---
print("=" * 60)
print("Neural Network: Handwritten Digit Recognition")
print("=" * 60)

digits = load_digits()
X = digits.data
y = digits.target

print(f"\nDataset shape: {X.shape}")
print(f"Each image: 8x8 pixels = 64 features")
print(f"Classes: digits 0-9")
print(f"Samples per class: {np.bincount(y)}")

# --- 2. Preprocess ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTraining samples: {X_train.shape[0]}")
print(f"Test samples: {X_test.shape[0]}")

# --- 3. Build and train the neural network ---
print("\nTraining neural network...")
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    activation="relu",
    solver="adam",
    max_iter=300,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1,
    verbose=False,
)
mlp.fit(X_train, y_train)

print(f"Network architecture: 64 -> 128 -> 64 -> 10")
print(f"Training iterations: {mlp.n_iter_}")
print(f"Final training loss: {mlp.loss_:.4f}")

# --- 4. Evaluate ---
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nTest Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --- 5. Visualizations ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Sample digit images with predictions
sample_indices = [0, 15, 30, 45, 60, 75, 90, 105]
ax_digits = axes[0, 0]
for idx, sample_idx in enumerate(sample_indices[:8]):
    row, col = divmod(idx, 4)
    x_offset = col * 10
    y_offset = row * 10
    img = digits.images[
        np.where(
            (digits.target == idx) if idx < 10 else (digits.target == idx % 10)
        )[0][0]
    ]
    for i in range(8):
        for j in range(8):
            ax_digits.add_patch(
                plt.Rectangle(
                    (x_offset + j, 18 - y_offset - i),
                    1,
                    1,
                    facecolor=plt.cm.gray_r(img[i, j] / 16),
                )
            )
    ax_digits.text(x_offset + 4, 19 - y_offset + 1.5, str(idx), ha="center", fontsize=8)
ax_digits.set_xlim(-1, 41)
ax_digits.set_ylim(-1, 22)
ax_digits.set_aspect("equal")
ax_digits.set_title("Sample Digits from Dataset")
ax_digits.axis("off")

# Training loss curve
axes[0, 1].plot(mlp.loss_curve_, color="steelblue", linewidth=2)
axes[0, 1].set_xlabel("Iteration")
axes[0, 1].set_ylabel("Loss")
axes[0, 1].set_title("Training Loss Curve")
axes[0, 1].grid(True, alpha=0.3)

# Predictions on test samples
test_original = scaler.inverse_transform(X_test)
n_show = 20
fig_pred, axes_pred = plt.subplots(2, 10, figsize=(15, 3))
for i in range(n_show):
    row = i // 10
    col = i % 10
    axes_pred[row, col].imshow(
        test_original[i].reshape(8, 8), cmap="gray_r", interpolation="nearest"
    )
    color = "green" if y_pred[i] == y_test[i] else "red"
    axes_pred[row, col].set_title(f"{y_pred[i]}", color=color, fontsize=10)
    axes_pred[row, col].axis("off")
fig_pred.suptitle(
    "Predictions (green=correct, red=wrong)", fontsize=12, y=1.02
)
fig_pred.tight_layout()
fig_pred.savefig("examples/output_neural_network_predictions.png", dpi=100, bbox_inches="tight")
plt.close(fig_pred)

# Per-class accuracy
class_acc = []
for digit in range(10):
    mask = y_test == digit
    if mask.sum() > 0:
        class_acc.append(accuracy_score(y_test[mask], y_pred[mask]))
    else:
        class_acc.append(0)
axes[1, 0].bar(range(10), class_acc, color="steelblue")
axes[1, 0].set_xlabel("Digit")
axes[1, 0].set_ylabel("Accuracy")
axes[1, 0].set_title("Per-Digit Accuracy")
axes[1, 0].set_xticks(range(10))
axes[1, 0].set_ylim(0.8, 1.02)

# Confidence distribution
proba = mlp.predict_proba(X_test)
max_confidence = proba.max(axis=1)
axes[1, 1].hist(max_confidence, bins=30, color="coral", edgecolor="black", alpha=0.7)
axes[1, 1].set_xlabel("Prediction Confidence")
axes[1, 1].set_ylabel("Count")
axes[1, 1].set_title("Confidence Distribution")
axes[1, 1].axvline(
    x=max_confidence.mean(),
    color="black",
    linestyle="--",
    label=f"Mean: {max_confidence.mean():.3f}",
)
axes[1, 1].legend()

plt.tight_layout()
plt.savefig("examples/output_neural_network.png", dpi=100)
plt.close()
print("\nPlots saved to examples/output_neural_network.png")
print("             examples/output_neural_network_predictions.png")
