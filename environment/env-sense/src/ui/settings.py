class Settings:
    def __init__(self):
        self.preferences = {
            "lighting": "default",
            "sound": "default",
            "workspace": "default"
        }

    def update_preference(self, key, value):
        if key in self.preferences:
            self.preferences[key] = value
            print(f"Updated {key} to {value}")
        else:
            print(f"Preference {key} does not exist.")

    def get_preferences(self):
        return self.preferences

    def reset_preferences(self):
        self.preferences = {
            "lighting": "default",
            "sound": "default",
            "workspace": "default"
        }
        print("Preferences reset to default.")