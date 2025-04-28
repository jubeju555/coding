import os
import json
import logging
import sqlite3
import pandas as pd
from datetime import datetime

class DataStorage:
    """Storage system for environment data and user preferences."""
    
    def __init__(self, db_path=None):
        """
        Initialize the storage system.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses default location.
        """
        self.logger = logging.getLogger("DataStorage")
        
        if not db_path:
            # Use default location in user's home directory
            home_dir = os.path.expanduser('~')
            data_dir = os.path.join(home_dir, '.env-sense')
            
            # Create directory if it doesn't exist
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            self.db_path = os.path.join(data_dir, 'environment-data.db')
        else:
            self.db_path = db_path
            
        # Initialize database
        self._init_database()
        
    def _init_database(self):
        """Initialize the SQLite database with necessary tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            
            # Environment data table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS environment_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                data TEXT
            )
            ''')
            
            # User preferences table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                settings TEXT,
                satisfaction REAL
            )
            ''')
            
            # Model data table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                version TEXT,
                parameters TEXT
            )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing database: {e}")
        finally:
            conn.close()
            
    def save_environment_data(self, timestamp, data):
        """Save environment data to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO environment_data (timestamp, data)
            VALUES (?, ?)
            ''', (timestamp, data))
            
            conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error saving environment data: {e}")
        finally:
            conn.close()
            
    def get_environment_data(self):
        """Retrieve all environment data from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM environment_data')
            rows = cursor.fetchall()
            
            return rows
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving environment data: {e}")
            return []
        finally:
            conn.close()
            
    def save_user_preferences(self, timestamp, settings, satisfaction):
        """Save user preferences to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO user_preferences (timestamp, settings, satisfaction)
            VALUES (?, ?, ?)
            ''', (timestamp, settings, satisfaction))
            
            conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error saving user preferences: {e}")
        finally:
            conn.close()
            
    def get_user_preferences(self):
        """Retrieve all user preferences from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM user_preferences')
            rows = cursor.fetchall()
            
            return rows
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving user preferences: {e}")
            return []
        finally:
            conn.close()
            
    def save_model(self, name, version, parameters):
        """Save model data to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO models (name, version, parameters)
            VALUES (?, ?, ?)
            ''', (name, version, parameters))
            
            conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error saving model data: {e}")
        finally:
            conn.close()
            
    def get_models(self):
        """Retrieve all models from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM models')
            rows = cursor.fetchall()
            
            return rows
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving models: {e}")
            return []
        finally:
            conn.close()