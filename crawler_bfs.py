import requests
import sqlite3
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
    crawl_queue = []
    
    # Check if the URL has been visited before
    if cursor.execute("SELECT url FROM visited WHERE url=?;", (url,)).fetchone():
        return crawl_queue
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
    except Exception as e:
        # Handle any exceptions that occur during the request
        print(e)
        return crawl_queue
    
    try:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Perform sentiment analysis on the webpage content
        distilled_student_sentiment_classifier_output = distilled_student_sentiment_classifier([soup.get_text().lower().replace('\n','').lstrip()])
        
        # Insert the visited URL into the 'visited' table
        cursor.execute("INSERT INTO visited (url) VALUES (?);", (url,))
        
        # Insert the webpage details into the 'webpages' table
        cursor.execute("INSERT INTO webpages (url, content, sentiment) VALUES (?, ?, ?);", (url, soup.get_text().lower().replace('\n','').lstrip(), distilled_student_sentiment_classifier_output[0][0]['score']))
        
        # Commit the changes to the database
        conn.commit()
    except Exception as e:
        # Handle any exceptions that occur during parsing or database operations
        print(e)

    # Extract all the links from the webpage and add them to the crawl queue
    for link in soup.find_all('a'):
        href = link.get('href')
        if href != None:   
            if href.startswith('/'):
                href = url + href
            elif not href.startswith('http'):
                continue
            crawl_queue.append(href)
    
    return crawl_queue