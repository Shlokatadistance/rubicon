"""Kalman filter for imputing/predicting off-market prices.

Functions:
- fit_kalman(returns, transition_matrix) -> KalmanFilter
- predict_missing(kf, observed_returns) -> np.ndarray
"""
import numpy as np

class KalmanFilter:
    def __init__(self, dt, state_variance, measurement_variance):
        self.dt = dt
        
        # 1. Initial State Estimate (Position, Velocity)
        self.x = np.matrix([[0.0], 
                            [0.0]])
        
        # 2. State Covariance Matrix (Uncertainty)
        self.P = np.matrix([[1.0, 0.0], 
                            [0.0, 1.0]])
        
        # 3. State Transition Matrix (Physics model: x = x + v*dt)
        self.F = np.matrix([[1.0, self.dt], 
                            [0.0, 1.0]])
        
        # 4. Measurement Matrix (We only measure position, not velocity)
        self.H = np.matrix([[1.0, 0.0]])
        
        # 5. Process Noise Covariance Matrix
        self.Q = np.matrix([[state_variance, 0.0], 
                            [0.0, state_variance]])
        
        # 6. Measurement Noise Covariance Matrix
        self.R = np.matrix([[measurement_variance]])
        
        # Identity Matrix
        self.I = np.eye(2)

    def predict(self):
        # x_k = F * x_{k-1}
        self.x = self.F * self.x
        # P_k = F * P_{k-1} * F^T + Q
        self.P = self.F * self.P * self.F.T + self.Q
        return self.x

    def update(self, z):
        # Innovation (Measurement residual): y = z - H * x
        y = z - self.H * self.x
        # Innovation covariance: S = H * P * H^T + R
        S = self.H * self.P * self.H.T + self.R
        # Optimal Kalman Gain: K = P * H^T * S^-1
        K = self.P * self.H.T * np.linalg.inv(S)
        
        # Update State Estimate: x = x + K * y
        self.x = self.x + K * y
        # Update State Covariance: P = (I - K * H) * P
        self.P = (self.I - K * self.H) * self.P

# --- Simulation / Testing ---
if __name__ == "__main__":
    # Simulate a car moving at a constant velocity of 2 m/s
    dt = 0.1
    kf = KalmanFilter(dt=dt, state_variance=0.1, measurement_variance=0.5)
    
    true_pos = 0.0
    true_vel = 2.0
    
    print("True Pos | Measured Pos | KF Estimated Pos")
    print("-" * 46)
    
    for _ in range(10):
        # Physics update
        true_pos += true_vel * dt
        # Add noise to simulate a real sensor measurement
        noisy_measurement = true_pos + np.random.normal(0, 0.5)
        
        # Kalman Filter Steps
        kf.predict()
        kf.update(noisy_measurement)
        
        print(f"{true_pos:8.2f} | {noisy_measurement:12.2f} | {kf.x[0,0]:16.2f}")