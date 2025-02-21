# NewsPulse AI Scraper

## Overview
**NewsPulse AI Scraper** is an automated web scraping system built with **Python**, **Selenium**, **Beautiful Soup**, and **ScrapeGraphAI**. It collects and summarizes articles from consulting firms' websites, extracting key information such as the title, author, publication date, and named entities.

## Why I Created NewsPulse AI Scraper
 created NewsPulse AI Scraper to automate the process of gathering and summarizing articles from consulting firms’ websites. Instead of manually browsing and extracting key insights, this tool leverages AI and web scraping to efficiently collect, analyze, and condense important information. By combining Selenium, Beautiful Soup, and OpenAI’s GPT model, the scraper provides structured data and concise summaries, making it easier to track industry trends and insights. This project enhances productivity, saves time, and helps professionals stay informed with minimal effort. 🚀

## Features
- 🔍 **Automated Web Scraping** – Uses Selenium to dynamically load and scroll through web pages.
- 📝 **Data Extraction** – Parses article content, metadata, and named entities using Beautiful Soup and spaCy.
- 🤖 **AI-Powered Summarization** – Utilizes OpenAI's GPT model to generate concise article summaries.
- 📂 **CSV Export** – Saves extracted data in a structured CSV file for further analysis.

## Technologies Used
- **Python**
- **Selenium**
- **Beautiful Soup**
- **ScrapeGraphAI**
- **OpenAI API** (for content summarization)
- **spaCy** (for named entity recognition)
- **Pandas** (for data storage and export)
- 
## 📂 Project Structure

This project consists of multiple scripts, each serving a unique purpose:

### 1️⃣ `mckinseyaiscraper.py`
- Scrapes articles exclusively from the **McKinsey** website.
- Uses **Selenium** and **BeautifulSoup** to extract article content, metadata, and named entities.
- Summarizes the extracted content using **OpenAI’s GPT model**.
- Outputs the results in a structured **CSV file**.

### 2️⃣ `googlenews.py`
- Allows users to **enter a prompt** in the terminal specifying the type of articles they are looking for.
- Searches **Google News** for the most relevant articles.
- Extracts and returns the **top search results** in a CSV file format, including titles, URLs, and summaries.
## Installation

###  Clone the repository
```bash
git clone git@github.com:yhuan331/Multi-Threaded-HTTP-Server.git
cd Multi-Threaded-HTTP-Server
```
### Create and activate a virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
### Usage
  a. Ensure you have a valid OpenAI API key and replace "your_openai_api_key_here" in the script with your actual API key.
  b. ensure you have all dependency installed 
	c.	Run the scraper:
  ```bash
  python scraper.py
  ```
### The script will:
- **Visit the McKinsey blog page**
- **Scroll to load all articles**
- **Extract article content and metadata**
- **Use AI to summarize each article**
- **Save the results to `scraped_articles_summary.csv`**

### Potential Enhancements 🚀
- Expand support to other consulting firms' websites
- Implement multi-threading for faster scraping
- Improve AI summarization by fine-tuning models for news articles
- Add a web interface for users to view and filter scraped articles
