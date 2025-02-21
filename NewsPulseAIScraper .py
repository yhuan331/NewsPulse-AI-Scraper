import csv
import requests
import pandas as pd
import spacy
import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up OpenAI API key and Spacy
openai.api_key = "your_openai_api_key_here"
nlp = spacy.load("en_core_web_sm")

def fetch_page_content_with_scrolling(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        html_content = driver.page_source
    except Exception as e:
        print(f"Error fetching the page: {e}")
        driver.quit()
        return None
    
    driver.quit()
    return html_content

def scrape_all_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = set()
    links = soup.find_all('a', href=True)
    
    for link in links:
        full_url = link['href']
        if not full_url.startswith("http"):
            full_url = f"https://www.mckinsey.com{full_url}"
        if "https://www.mckinsey.com/about-us/new-at-mckinsey-blog/" in full_url:
            urls.add(full_url)
    
    return list(urls)

def fetch_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def parse_article(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    result = {'url': url, 'title': 'Unknown', 'author': 'Unknown', 'publication_date': 'Unknown', 'content': 'Unknown', 'names': []}
    
    try:
        title_tag = soup.find('h1')
        if title_tag:
            result['title'] = title_tag.get_text(strip=True)
        
        author_tag = soup.find('meta', {'name': 'author'})
        if author_tag and 'content' in author_tag.attrs:
            result['author'] = author_tag['content']
        
        date_tag = soup.find('time')
        if date_tag:
            result['publication_date'] = date_tag.get_text(strip=True)
        
        paragraphs = soup.find_all('p')
        if paragraphs:
            content = ' '.join(p.get_text(strip=True) for p in paragraphs)
            result['content'] = content
            result['names'] = extract_names(content)
        
    except Exception as e:
        print(f"Error parsing HTML from {url}: {str(e)}")
    
    return result

def extract_names(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON' and ent.text.lower() != 'mckinsey']
    return names

def summarize_content(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Summarize the following text in 2-4 sentences."},
                      {"role": "user", "content": content}],
            max_tokens=150,
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error summarizing content: {str(e)}")
        return "Summary unavailable"

def main():
    main_blog_url = 'https://www.mckinsey.com/about-us/new-at-mckinsey-blog'
    html_content = fetch_page_content_with_scrolling(main_blog_url)
    if html_content:
        urls = scrape_all_urls(html_content)
        if urls:
            results = []
            for url in urls:
                html = fetch_article(url)
                if html:
                    article_data = parse_article(html, url)
                    if article_data and article_data['content']:
                        summary = summarize_content(article_data['content'])
                        data_to_save = {
                            'url': article_data['url'],
                            'title': article_data['title'],
                            'author': article_data['author'],
                            'publication_date': article_data['publication_date'],
                            'summary': summary,
                            'names': ', '.join(article_data['names'])
                        }
                        results.append(data_to_save)
            df_results = pd.DataFrame(results)
            df_results.to_csv('scraped_articles_summary.csv', index=False)
            print("Results saved to 'scraped_articles_summary.csv'.")
        else:
            print("No URLs found on the page.")
    else:
        print("Failed to fetch HTML content.")

if __name__ == "__main__":
    main()
