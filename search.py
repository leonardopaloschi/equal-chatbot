import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

def search_database(query):
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    tokens = word_tokenize(query.lower())

    results = []
    for token in tokens:
        synsets = wn.synsets(token)
        for synset in synsets:
            for lemma in synset.lemmas():
                keyword = lemma.name().lower()
                c.execute("SELECT * FROM webpages WHERE content LIKE '%' || ? || '%'", (keyword,))
                rows = c.fetchall()
                results.extend(rows)

    conn.close()

    return results