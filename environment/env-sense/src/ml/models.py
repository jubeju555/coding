from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

class UserPreferenceModel:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.scaler = StandardScaler()

    def train(self, features, targets):
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled, targets)

    def predict(self, features):
        features_scaled = self.scaler.transform(features)
        return self.model.predict(features_scaled)

    def save_model(self, filepath):
        import joblib
        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        import joblib
        self.model = joblib.load(filepath)