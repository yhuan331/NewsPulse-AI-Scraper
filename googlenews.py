
import requests
from bs4 import BeautifulSoup
from scrapegraphai.graphs import SearchGraph
from pydantic import BaseModel, Field
import pandas as pd
from urllib.parse import urlparse, unquote
import re

# Define schema for article metadata
class NewsArticle(BaseModel):
    title: str = Field(description="Title of the news article")
    url: str = Field(description="URL of the news article")
    publication_date: str = Field(description="Publication date of the article")
    author: str = Field(description="Author of the article, if available")
    summary: str = Field(description="Summary of the article content")

# scrapegraphai configuration
graph_config = {
    "llm": {
        "api_key": ''  # Replace with your actual API key
        "model": "openai/gpt-4",
    },
    "max_results": 1,
    "verbose": True,
}

def validate_url(url, target_site):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ["http", "https"] and target_site in parsed_url.netloc

def parse_article_content(url):
    prompt = f"Retrieve metadata such as title, summary, publication date, and author from the article available at {url}."
    search_graph = SearchGraph(prompt=prompt, config=graph_config, schema=NewsArticle)
    
    try:
        result = search_graph.run()
        if result:
            return result
        else:
            print(f"No results from scrapegraphai for {url}, attempting fallback parsing.")
            return fallback_parse_with_bs4(url)
    except Exception as e:
        print(f"Error occurred while parsing {url} with scrapegraphai: {e}")
        return fallback_parse_with_bs4(url)

def fallback_parse_with_bs4(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No Title"
        
        # Improved summary extraction using meta tag
        summary_tag = soup.find("meta", {"name": "description"})
        summary = summary_tag["content"] if summary_tag else "No Summary"
        
        # Extract publication date
        publication_date = soup.find("time").get_text(strip=True) if soup.find("time") else "No Date"
        
        # Improved author extraction
        author_tag = soup.find("meta", {"name": "author"}) or \
                     soup.find("span", class_=re.compile("author|byline", re.I)) or \
                     soup.find("div", class_=re.compile("author|byline", re.I)) or \
                     soup.find("a", class_=re.compile("author|byline", re.I))
        author = author_tag.get_text(strip=True) if author_tag else "No Author"

        # Existing extraction logic for people remains unchanged
        cited_individuals = []
        article_text = soup.get_text(separator=" ", strip=True)
        pattern = r"([A-Z][a-z]+\s[A-Z][a-z]+)\s(?:from|at|,)\s([\w\s]+)"
        matches = re.findall(pattern, article_text)
        for name, affiliation in matches:
            cited_individuals.append(f"{name} from {affiliation}")
        cited_individuals_text = "; ".join(cited_individuals) if cited_individuals else "No cited individuals"

        return {
            "url": url,
            "title": title,
            "summary": summary,
            "publication_date": publication_date,
            "author": author,
            "cited_individuals": cited_individuals_text
        }
    except Exception as e:
        print(f"Error occurred in fallback parsing for {url}: {e}")
        return {
            "url": url,
            "title": "No Title",
            "summary": "No Summary",
            "publication_date": "No Date",
            "author": "No Author",
            "cited_individuals": "No cited individuals"
        }

def simple_scrape_urls(topic, target_sites):
    results = []
    for site in target_sites:
        query = f"{topic} site:{site}"
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "url?q=" in href:
                url = href.split("url?q=")[1].split("&")[0]
                url = unquote(url)  
                if validate_url(url, site):
                    results.append({"url": url})
    return results

def main():
    topic = input("Enter a topic: ")
    websites = ["mckinsey.com", "deloitte.com", "bain.com"]  # Add more websites as needed

    all_articles = []
    
    for site in websites:
        print(f"\nSearching articles for '{topic}' on {site}...\n")
        urls = simple_scrape_urls(topic, [site])
        
        for url in urls:
            print(f"Processing {url['url']}")
            article_data = parse_article_content(url['url'])
            if article_data:
                all_articles.append(article_data)

    if all_articles:
        df = pd.DataFrame(all_articles)
        df.to_csv("new.csv", index=False)
        print("Article details saved to new.csv")
    else:
        print("No articles were parsed successfully.")

if __name__ == "__main__":
    main()