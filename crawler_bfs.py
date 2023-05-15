import requests
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

async def crawl_bfs(url):
    crawl_queue = []
    if cursor.execute("SELECT url FROM visited WHERE url=?;", (url,)).fetchone():
        return crawl_queue
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return crawl_queue
    soup = BeautifulSoup(response.text, 'html.parser')
    cursor.execute("INSERT INTO webpages (url, content) VALUES (?, ?);", (url, soup.get_text().lower().replace('\n','')))
    conn.commit()
    for link in soup.find_all('a'):
        href = link.get('href')
        if href != None:   
            if href.startswith('/'):
                href = url + href
            elif not href.startswith('http'):
                continue
            crawl_queue.append(href)
    
    return crawl_queue