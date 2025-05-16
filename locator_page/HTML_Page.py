from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime

# Setup Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    url = "https://www.southwest.com"
    driver.get(url)
    time.sleep(3)  # Let the page load

    # Save full HTML to file
    html = driver.page_source
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Count IFrames using Selenium
    iframe_count = len(driver.find_elements(By.TAG_NAME, "iframe"))

    # Count Shadow DOM roots using JavaScript
    shadow_count = driver.execute_script("""
        let count = 0;
        function countShadowRoots(element) {
            if (element.shadowRoot) count++;
            if (element.children && element.children.length > 0) {
                [...element.children].forEach(countShadowRoots);
            }
        }
        countShadowRoots(document.documentElement);
        return count;
    """)

    # Use BeautifulSoup for other tag counts
    soup = BeautifulSoup(html, "html.parser")
    form_count = len(soup.find_all("form"))
    input_count = len(soup.find_all("input"))
    button_count = len(soup.find_all("button"))

    # Write Markdown summary
    with open("dump_analysis.md", "w", encoding="utf-8") as md:
        md.write("# Page Dump Analysis\n\n")
        md.write(f"**URL:** `{url}`  \n")
        md.write(f"**Timestamp:** {datetime.datetime.now()}  \n\n")
        md.write("| Element Type | Count |\n")
        md.write("|--------------|-------|\n")
        md.write(f"| iframe       | {iframe_count} |\n")
        md.write(f"| shadow-root  | {shadow_count} |\n")
        md.write(f"| form         | {form_count} |\n")
        md.write(f"| input        | {input_count} |\n")
        md.write(f"| button       | {button_count} |\n")

    print("✅ Dump and analysis complete. See 'dump_analysis.md'.")

finally:
    driver.quit()

