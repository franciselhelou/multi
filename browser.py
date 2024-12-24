import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def initialize_driver():
    """Initialize and return a WebDriver instance."""
    options = Options()
    #options.add_argument("--incognito")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def perform_search_google(query, number_of_results=None):
    driver = initialize_driver()

    try:
        # Open Google
        driver.get("https://www.google.com")

        # Locate the search bar, enter query, and hit ENTER
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load
        time.sleep(3)

        # Extract the top search results
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")

        # Collect titles and URLs
        search_results = []
        for result in results:  # Get top 5 results
            title = result.find_element(By.TAG_NAME, "h3").text
            url = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            search_results.append({"title": title, "url": url})

        return search_results

    finally:
        # Close the browser
        driver.quit()

        

        
def scrape_content(url):
    """Scrape the content from the given URL."""
    try:
        # Send a GET request to retrieve the HTML content of the page
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Use BeautifulSoup for advanced parsing
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Attempt to extract content based on common tags
        content = ""
        
        # First, try extracting paragraphs
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])

        # If no content in paragraphs, attempt to extract <article> or <div> tags with main content
        if not content:
            articles = soup.find_all("article")
            content = "\n".join([a.get_text() for a in articles if a.get_text()])
        
        # If still no content, fall back to a common content div, if available
        if not content:
            divs = soup.find_all("div", {"class": "content"})
            content = "\n".join([div.get_text() for div in divs if div.get_text()])

        # Return the content or a message if none found
        return content if content else "No significant content found."

    except Exception as e:
        print(f"Error scraping content for {url}: {e}")
        return "Failed to retrieve content."

def save_content(urls, filename="scraped_content.txt"):
    """Save scraped content from multiple URLs to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for url in urls:
            # Scrape the content from each URL
            content = scrape_content(url)
            
            # Write the URL and its content to the file
            file.write(f"URL: {url}\n\n")
            file.write(f"{content}\n\n{'-'*80}\n\n")  # Add a separator between entries
            print(f"Content from {url} saved.")

    print(f"All content saved to {filename}")

    