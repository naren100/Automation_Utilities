import yaml
import os

class URLManager:
    def __init__(self, config_path=None):
        default_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'urls.yaml')
        self.config_path = config_path or default_path
        self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        env = self.config.get('env', 'prod')
        self.base_url = self.config['environments'][env]['base_url']
        self.routes = self.config['urls']

    def get_url(self, key):
        if key not in self.routes:
            raise ValueError(f"[URL ERROR] No path found for key: {key}")
        return self.base_url + self.routes[key]
