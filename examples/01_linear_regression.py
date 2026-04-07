"""
Linear Regression Example
=========================
Predict housing prices using a simple linear regression model.

Concepts covered:
- Loading and exploring data
- Train/test split
- Fitting a linear regression model
- Evaluating with MSE and R² score
- Visualizing predictions vs actual values
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# --- 1. Load the dataset ---
print("=" * 60)
print("Linear Regression: California Housing Prices")
print("=" * 60)

housing = fetch_california_housing()
X = housing.data
y = housing.target
feature_names = housing.feature_names

print(f"\nDataset shape: {X.shape}")
print(f"Features: {feature_names}")
print(f"Target: Median house value (in $100,000s)")
print(f"Sample target values: {y[:5]}")

# --- 2. Split into training and test sets ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining samples: {X_train.shape[0]}")
print(f"Test samples: {X_test.shape[0]}")

# --- 3. Train the model ---
model = LinearRegression()
model.fit(X_train, y_train)

print("\nModel coefficients:")
for name, coef in zip(feature_names, model.coef_):
    print(f"  {name:>12}: {coef:+.4f}")
print(f"  {'Intercept':>12}: {model.intercept_:+.4f}")

# --- 4. Make predictions and evaluate ---
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"\nModel Performance:")
print(f"  Mean Squared Error:  {mse:.4f}")
print(f"  Root MSE:            {rmse:.4f}")
print(f"  R² Score:            {r2:.4f}")

# --- 5. Visualize predictions vs actual ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scatter plot: predicted vs actual
axes[0].scatter(y_test, y_pred, alpha=0.3, s=10, color="steelblue")
axes[0].plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--",
    linewidth=2,
    label="Perfect prediction",
)
axes[0].set_xlabel("Actual Price ($100k)")
axes[0].set_ylabel("Predicted Price ($100k)")
axes[0].set_title("Predicted vs Actual House Prices")
axes[0].legend()

# Residual plot
residuals = y_test - y_pred
axes[1].scatter(y_pred, residuals, alpha=0.3, s=10, color="coral")
axes[1].axhline(y=0, color="black", linestyle="--", linewidth=1)
axes[1].set_xlabel("Predicted Price ($100k)")
axes[1].set_ylabel("Residual")
axes[1].set_title("Residual Plot")

plt.tight_layout()
plt.savefig("examples/output_linear_regression.png", dpi=100)
plt.close()
print("\nPlot saved to examples/output_linear_regression.png")
