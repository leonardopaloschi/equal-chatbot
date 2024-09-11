"""
This module performs web crawling using a breadth-first search (BFS) approach.
It crawls a given URL, analyzes the sentiment of the webpage content using a sentiment analysis pipeline,
and stores the results in an SQLite database.

Dependencies:
- aiohttp: For asynchronous HTTP requests.
- BeautifulSoup: For parsing HTML content.
- transformers: For sentiment analysis.
- sqlite3: For database operations.
"""

import sqlite3
import aiohttp
from bs4 import BeautifulSoup
from transformers import pipeline

# Initialize the sentiment classifier pipeline
distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    return_all_scores=True
)

# Connect to the SQLite database
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

async def crawl_bfs(url):
    """
    Perform breadth-first search to crawl the given URL, analyze its sentiment, and store the data in the SQLite database.

    Args:
        url (str): The URL to crawl.

    Returns:
        list: List of URLs to crawl next.
    """
    crawl_queue = []

    if cursor.execute("SELECT url FROM visited WHERE url=?;", (url,)).fetchone():
        return crawl_queue

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return crawl_queue

    try:
        soup = BeautifulSoup(html, 'html.parser')
        text_content = soup.get_text().lower().replace('\n', '').strip()
        sentiment_output = distilled_student_sentiment_classifier([text_content])

        cursor.execute("INSERT INTO visited (url) VALUES (?);", (url,))
        cursor.execute(
            "INSERT INTO webpages (url, content, sentiment) VALUES (?, ?, ?);",
            (url, text_content, sentiment_output[0][0]['score'])
        )
        conn.commit()
    except (sqlite3.DatabaseError, Exception) as e:
        print(f"Parsing or DB operation failed: {e}")

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            if href.startswith('/'):
                href = url + href
            elif not href.startswith('http'):
                continue
            crawl_queue.append(href)

    return crawl_queue
