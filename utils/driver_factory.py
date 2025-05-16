import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverFactory:

    @staticmethod
    def load_config():
        config_path = os.path.join(os.path.dirname(__file__), '../configs/browser_config.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    @staticmethod
    def get_driver():
        config = DriverFactory.load_config()
        browser = config.get("browser", "chrome").lower()
        headless = config.get("headless", True)
        remote_url = config.get("remote_url")

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )

        elif browser == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            return webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )

        elif browser == "safari":
            # Safari has no headless mode and requires macOS
            return webdriver.Safari()

        elif browser == "remote":
            if not remote_url:
                raise ValueError("Missing 'remote_url' in config for remote browser.")
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            return webdriver.Remote(
                command_executor=remote_url,
                options=options
            )

        else:
            raise ValueError(f"Unsupported browser: {browser}")

