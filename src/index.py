import random
import time


class KalmanFilter:
    def __init__(self, process_noise_cov, measurement_noise_cov, initial_estimate, initial_cov):
        self.Q = process_noise_cov  # Process noise covariance
        self.R = measurement_noise_cov  # Measurement noise covariance
        self.x_est = initial_estimate  # Initial state estimate
        self.P = initial_cov  # Initial error covariance

    def predict(self):
        # Predict step
        self.P_pred = self.P + self.Q  # Predict error covariance

    def update(self, measurement):
        # Update step
        K = self.P_pred / (self.P_pred + self.R)  # Dynamic Kalman Gain
        self.K = K
        self.x_est = self.x_est + K * (measurement - self.x_est)  # Update estimate using measurement
        self.P = (1 - K) * self.P_pred  # Update error covariance

        return self.x_est  # Return the updated estimate


# Example Usage
if __name__ == "__main__":
    # Initialize the Kalman filter for x_err
    kf = KalmanFilter(
        process_noise_cov=0.1,  # Tune this value
        measurement_noise_cov=1.0,  # Tune this value
        initial_estimate=0,  # Initial horizontal error estimate
        initial_cov=1  # Initial error covariance
    )

    # Simulated measurements of x_err from a sensor
    measurements = [1.0, 2.0, 1.5, 3.0, 2.5]  # Example x_err values

    while True:
        kf.predict()  # Perform the predict step
        x_err = random.uniform(-0.5, 0.5)
        updated_estimate = kf.update(x_err)  # Perform the update step
        print(f"original x_err: {x_err:.2f}")
        print(f"Updated Estimate of x_err: {updated_estimate:.2f}")
        print(f"Updated Estimate of P: {kf.P:.2f}")
        print(f"Updated Estimate of Q: {kf.Q:.2f}")
        print(f"Updated Estimate of R: {kf.R:.2f}")
        print(f"Updated Estimate of K: {kf.K:.2f}")
        # time.sleep(0.5)
        # for measurement in measurements:
        #     kf.predict()  # Perform the predict step
        #     updated_estimate = kf.update(measurement)  # Perform the update step
        #     print(f"Updated Estimate of x_err: {updated_estimate:.2f}")
        #     print(f"Updated Estimate of P: {kf.P:.2f}")
        #     print(f"Updated Estimate of Q: {kf.Q:.2f}")
        #     print(f"Updated Estimate of R: {kf.R:.2f}")