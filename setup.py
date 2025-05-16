from setuptools import setup, find_packages

setup(
    name="automation_utilities",
    version="0.1.0",
    description="Reusable automation tools (Selenium, locators, config)",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0",
        "webdriver-manager>=3.0",
        "beautifulsoup4>=4.11"
    ],
)
