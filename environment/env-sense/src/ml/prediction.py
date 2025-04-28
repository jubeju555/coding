import logging
import numpy as np
import pandas as pd
from datetime import datetime
from .models import UserPreferenceModel

class PredictionEngine:
    """Engine for making predictions about user preferences."""
    
    def __init__(self, model):
        """
        Initialize the prediction engine.
        
        Args:
            model: The trained ML model for predictions
        """
        self.model = model
        self.logger = logging.getLogger("PredictionEngine")
        
    def predict(self, features):
        """
        Make a prediction based on the input features.
        
        Args:
            features (dict): Environment features
            
        Returns:
            dict: Predicted preferences
        """
        try:
            # Convert features to DataFrame for prediction
            features_df = pd.DataFrame([features])
            
            # Make prediction
            prediction = self.model.predict(features_df)
            
            # Convert numerical predictions to settings
            settings = self._interpret_prediction(prediction)
            
            self.logger.debug(f"Predicted settings: {settings}")
            return settings
            
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            return {}
            
    def _interpret_prediction(self, prediction):
        """
        Convert raw numerical predictions to environment settings.
        
        Args:
            prediction: Raw numerical predictions from the model
            
        Returns:
            dict: Environment settings
        """
        try:
            # This would be more sophisticated in production
            # Here we're converting the raw prediction values to settings
            
            # Example mapping:
            settings = {
                'lighting_brightness': max(0, min(100, int(prediction[0][0]))),
                'sound_volume': max(0, min(100, int(prediction[0][1]))),
                'temperature': max(18, min(26, int(prediction[0][2]))),
            }
            
            # Convert categorical features from numerical
            app_arrangement_types = ['default', 'focused', 'productive', 'relaxed']
            app_arrangement_idx = max(0, min(len(app_arrangement_types)-1, int(prediction[0][3])))
            settings['app_arrangement'] = app_arrangement_types[app_arrangement_idx]
            
            desktop_types = ['default', 'focused', 'productive', 'relaxed']
            desktop_idx = max(0, min(len(desktop_types)-1, int(prediction[0][4])))
            settings['desktop_arrangement'] = desktop_types[desktop_idx]
            
            self.logger.debug(f"Interpreted {prediction} as {settings}")
            return settings
            
        except Exception as e:
            self.logger.error(f"Error interpreting prediction: {e}")
            return {}
            
    def get_explanation(self, features, prediction):
        """
        Get an explanation for the prediction.
        
        Args:
            features (dict): Input features
            prediction (dict): Model prediction
            
        Returns:
            str: Explanation of the prediction
        """
        try:
            # This is a simplified explanation generator
            # In production, you'd use tools like LIME or SHAP
            
            explanation = "Environment adjusted based on:\n"
            
            # Time-based explanation
            if 'time_hour' in features:
                hour = features['time_hour']
                if 5 <= hour < 12:
                    explanation += "- Morning hours (optimizing for productivity)\n"
                elif 12 <= hour < 17:
                    explanation += "- Afternoon hours (balanced settings)\n"
                elif 17 <= hour < 22:
                    explanation += "- Evening hours (optimizing for comfort)\n"
                else:
                    explanation += "- Night hours (reduced brightness)\n"
                    
            # System usage explanation
            if 'system_cpu_usage' in features:
                cpu = features['system_cpu_usage']
                if cpu > 80:
                    explanation += "- High CPU usage (optimizing for performance)\n"
                    
            # Calendar-based explanation
            if 'calendar_has_current_meeting' in features and features['calendar_has_current_meeting']:
                explanation += "- Ongoing meeting detected (optimizing for communication)\n"
                
            return explanation
            
        except Exception as e:
            self.logger.error(f"Error generating explanation: {e}")
            return "No explanation available"

def predict_user_preferences(user_data):
    """
    Predicts user preferences based on the provided user data using the trained model.

    Parameters:
    user_data (dict): A dictionary containing user data for prediction.

    Returns:
    dict: A dictionary containing predicted preferences.
    """
    model = UserPreferenceModel()
    engine = PredictionEngine(model)
    predictions = engine.predict(user_data)
    return predictions

def adjust_environment(predictions):
    """
    Adjusts the environment settings based on the predicted user preferences.

    Parameters:
    predictions (dict): A dictionary containing predicted preferences.
    """
    # Logic to adjust environment settings based on predictions
    # This could involve calling functions from the adapters module
    pass