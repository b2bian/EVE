import json
import os

class ThemeLoader:
    """Loads and manages the application theme."""
    
    def __init__(self, config_file="style_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                return self._get_default_config()
        return self._get_default_config()
    
    def _get_default_config(self):
        """Return default configuration."""
        return {
            "theme": {
                "appearance_mode": "Dark",
                "colors": {
                    "background": "#1a1a1a",
                    "secondary_bg": "#0f0f0f",
                    "accent_cyan": "#00f2ff",
                    "accent_orange": "#ff9d00",
                    "warning": "#ff3333",
                    "success": "#00ff00",
                    "text_primary": "#ffffff",
                    "text_secondary": "#888888",
                    "border": "#333333"
                }
            },
            "ui": {
                "corner_radius": 2,
                "border_width": 1,
                "padding": 8,
                "spacing": 4,
                "font_size_title": 14,
                "font_size_normal": 12,
                "font_size_small": 10,
                "font_family": "Courier New"
            }
        }
    
    def get_color(self, color_name):
        """Get color value by name."""
        colors = self.config.get("theme", {}).get("colors", {})
        return colors.get(color_name, "#ffffff")
    
    def get_ui_value(self, key):
        """Get UI configuration value."""
        ui = self.config.get("ui", {})
        return ui.get(key)
    
    def get_appearance_mode(self):
        """Get appearance mode (Dark/Light)."""
        return self.config.get("theme", {}).get("appearance_mode", "Dark")
    
    def get_font_size(self, size_type="normal"):
        """Get font size."""
        ui = self.config.get("ui", {})
        key = f"font_size_{size_type}"
        return ui.get(key, 12)
    
    def get_font_family(self):
        """Get font family."""
        ui = self.config.get("ui", {})
        return ui.get("font_family", "Courier New")
    
    def get_config(self):
        """Get entire configuration."""
        return self.config
    
    def save_config(self, config=None):
        """Save configuration to file."""
        config_to_save = config if config else self.config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            self.config = config_to_save
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def update_color(self, color_name, hex_value):
        """Update a color in the configuration."""
        if "theme" not in self.config:
            self.config["theme"] = {}
        if "colors" not in self.config["theme"]:
            self.config["theme"]["colors"] = {}
        
        self.config["theme"]["colors"][color_name] = hex_value
        self.save_config()
