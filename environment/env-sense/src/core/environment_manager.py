import logging
import time
import threading
from datetime import datetime

class EnvironmentManager:
    """Central coordinator for the personalized environment system."""
    
    def __init__(self, data_collectors, preference_engine, adapters):
        """
        Initialize the environment manager.
        
        Args:
            data_collectors (list): List of collector objects that gather environmental data
            preference_engine: Engine that determines user preferences
            adapters (list): List of adapter objects that can modify the environment
        """
        self.data_collectors = data_collectors
        self.preference_engine = preference_engine
        self.adapters = adapters
        self.running = False
        self.monitoring_thread = None
        self.adjustment_frequency = 60  # seconds between environment checks
        self.logger = logging.getLogger("EnvironmentManager")
        
    def start(self):
        """Start the environment monitoring and adjustment system."""
        if self.running:
            return
            
        self.running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        self.logger.info("Environment manager started")
        
    def stop(self):
        """Stop the environment monitoring and adjustment system."""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        self.logger.info("Environment manager stopped")
        
    def _monitoring_loop(self):
        """Main loop that periodically checks and adjusts the environment."""
        while self.running:
            try:
                # 1. Collect current environment data
                current_data = {}
                for collector in self.data_collectors:
                    current_data.update(collector.collect())
                
                # 2. Get recommended settings
                recommendations = self.preference_engine.get_recommendations(current_data)
                
                # 3. Apply changes through adapters
                for adapter in self.adapters:
                    relevant_settings = {k: v for k, v in recommendations.items() 
                                        if k in adapter.supported_settings()}
                    if relevant_settings:
                        adapter.apply_settings(relevant_settings)
                
                # 4. Record user feedback (if any)
                # This would be handled via UI events
                
                # Log activity
                self.logger.debug(f"Environment adjusted at {datetime.now()}")
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
            
            # Sleep until next check
            time.sleep(self.adjustment_frequency)