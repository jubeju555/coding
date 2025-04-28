import logging
import numpy as np
import pandas as pd
from datetime import datetime
from ..ml.models import UserPreferenceModel
from ..data.storage import DataStorage

class PreferenceEngine:
    """Engine for determining user preferences based on collected data."""
    
    def __init__(self, storage, model=None):
        """
        Initialize the preference engine.
        
        Args:
            storage: DataStorage instance for retrieving and storing preference data
            model: Optional pre-trained model
        """
        self.storage = storage
        self.model = model if model else UserPreferenceModel()
        self.logger = logging.getLogger("PreferenceEngine")
        self.last_training_time = None
        self.training_frequency_hours = 12  # Retrain model every 12 hours
        self.default_preferences = {
            'lighting_brightness': 75,  # percentage
            'sound_volume': 50,         # percentage
            'temperature': 22,          # celsius
            'app_arrangement': 'default',
            'desktop_arrangement': 'default'
        }
        
    def get_recommendations(self, current_data):
        """
        Get environment setting recommendations based on current data.
        
        Args:
            current_data (dict): Current environmental data
            
        Returns:
            dict: Recommended environment settings
        """
        # Check if model needs training or retraining
        if self._should_train_model():
            self._train_model()
        
        try:
            # Prepare features for prediction
            features = self._prepare_features(current_data)
            
            # Get model predictions if model is available
            if self.model and hasattr(self.model, 'predict'):
                predictions = self.model.predict(features)
                
                # Convert predictions to recommendation dict
                recommendations = self._convert_predictions_to_recommendations(predictions)
            else:
                # Use default preferences if no model is available
                recommendations = self.default_preferences.copy()
            
            # Log and return recommendations
            self.logger.debug(f"Generated recommendations: {recommendations}")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return self.default_preferences.copy()
    
    def record_feedback(self, settings, satisfaction_score):
        """
        Record user feedback about current environment settings.
        
        Args:
            settings (dict): Current environment settings
            satisfaction_score (float): User's satisfaction score (0-100)
        """
        try:
            # Log satisfaction score
            self.logger.info(f"User satisfaction: {satisfaction_score}")
            
            # Store settings and score
            data = {**settings, 'satisfaction': satisfaction_score, 'timestamp': datetime.now()}
            self.storage.store_feedback(data)
            
            # Check if model should be retrained
            if satisfaction_score < 50:  # Low satisfaction might trigger immediate retraining
                self._train_model(force=True)
                
        except Exception as e:
            self.logger.error(f"Error recording feedback: {e}")
    
    def _should_train_model(self):
        """Check if the model needs training based on last training time or data volume."""
        if not self.last_training_time:
            return True
            
        hours_since_training = (datetime.now() - self.last_training_time).total_seconds() / 3600
        if hours_since_training >= self.training_frequency_hours:
            return True
            
        # Check if enough new data is available
        new_data_count = self.storage.count_new_data(self.last_training_time)
        if new_data_count > 20:  # Retrain if we have 20+ new data points
            return True
            
        return False
        
    def _train_model(self, force=False):
        """Train or retrain the preference model using stored data."""
        try:
            # Get training data from storage
            training_data = self.storage.get_training_data()
            
            if len(training_data) < 10 and not force:
                self.logger.info("Not enough data to train model")
                return False
                
            # Prepare features and targets
            features = pd.DataFrame([d['features'] for d in training_data])
            targets = pd.DataFrame([d['preferences'] for d in training_data])
            
            # Train the model
            self.model.train(features, targets)
            
            # Update last training time
            self.last_training_time = datetime.now()
            self.logger.info(f"Model trained with {len(training_data)} data points")
            return True
            
        except Exception as e:
            self.logger.error(f"Error training model: {e}")
            return False
    
    def _prepare_features(self, current_data):
        """Prepare features for model prediction."""
        # Extract relevant features
        features = {}
        
        # Time features
        if 'time_hour' in current_data:
            features['time_hour'] = current_data['time_hour']
            features['time_minute'] = current_data.get('time_minute', 0)
            features['time_day_of_week'] = current_data.get('time_day_of_week', 0)
            features['time_is_weekend'] = current_data.get('time_is_weekend', 0)
        
        # System features
        if 'system_cpu_usage' in current_data:
            features['system_cpu_usage'] = current_data['system_cpu_usage']
            features['system_memory_usage'] = current_data.get('system_memory_usage', 50)
            features['system_battery'] = current_data.get('system_battery', 100)
        
        # Calendar features
        if 'calendar_has_current_meeting' in current_data:
            features['calendar_has_current_meeting'] = int(current_data['calendar_has_current_meeting'])
            features['calendar_next_meeting_in_minutes'] = current_data.get('calendar_next_meeting_in_minutes', 1440)
        
        # Return as DataFrame for model
        return pd.DataFrame([features])
    
    def _convert_predictions_to_recommendations(self, predictions):
        """Convert model predictions to recommendation dictionary."""
        # Map prediction vector to named settings
        recommendations = {}
        
        # This is simplified - in production, you would have a more robust mapping
        setting_names = ['lighting_brightness', 'sound_volume', 'temperature', 'app_arrangement', 'desktop_arrangement']
        
        # Convert predictions to appropriate types
        for i, name in enumerate(setting_names):
            if i < len(predictions[0]):
                value = predictions[0][i]
                
                # Handle different data types
                if name in ['lighting_brightness', 'sound_volume']:
                    # Ensure values are between 0-100
                    recommendations[name] = max(0, min(100, int(value)))
                elif name == 'temperature':
                    # Reasonable temperature range
                    recommendations[name] = max(18, min(26, int(value)))
                elif name in ['app_arrangement', 'desktop_arrangement']:
                    # Convert numerical values to arrangement types
                    arrangement_types = ['default', 'focused', 'relaxed', 'productive']
                    idx = max(0, min(len(arrangement_types) - 1, int(value)))
                    recommendations[name] = arrangement_types[idx]
                else:
                    recommendations[name] = value
        
        # Fill in missing values with defaults
        for key, default_value in self.default_preferences.items():
            if key not in recommendations:
                recommendations[key] = default_value
        
        return recommendations