import logging
import sys
import time
import threading
import os
from datetime import datetime

# Import core components
from core.environment_manager import EnvironmentManager
from core.preference_engine import PreferenceEngine
from core.system_interface import SystemInterface

# Import data components
from data.collectors import TimeCollector, WindowsSystemCollector, CalendarCollector
from data.storage import DataStorage

# Import adapters
from adapters.lighting import LightingAdapter
from adapters.sound import SoundAdapter
from adapters.workspace import WorkspaceAdapter

def setup_logging():
    """Configure logging for the application."""
    log_dir = os.path.join(os.path.expanduser("~"), ".env-sense", "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, f"env-sense-{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("main")

def main():
    """Main application entry point."""
    logger = setup_logging()
    logger.info("Starting Personal Environment Manager")
    
    # Initialize components
    try:
        # Initialize storage
        storage = DataStorage()
        
        # Initialize collectors
        collectors = [
            TimeCollector(),
            WindowsSystemCollector(),
            CalendarCollector()
        ]
        
        # Initialize preference engine
        preference_engine = PreferenceEngine(storage)
        
        # Initialize adapters
        adapters = [
            LightingAdapter(),
            SoundAdapter(),
            WorkspaceAdapter()
        ]
        
        # Initialize environment manager
        env_manager = EnvironmentManager(collectors, preference_engine, adapters)
        
        # Start the environment manager
        env_manager.start()
        
        logger.info("Environment manager started successfully")
        
        # Keep the main thread running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            env_manager.stop()
            
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())