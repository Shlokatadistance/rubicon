"""Kalman filter for imputing/predicting off-market prices.

Functions:
- fit_kalman(returns, transition_matrix) -> KalmanFilter
- predict_missing(kf, observed_returns) -> np.ndarray
"""
