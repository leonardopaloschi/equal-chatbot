"""
Este módulo realiza buscas na tabela 'webpages' de um banco de dados SQLite usando termos
relacionados a uma consulta fornecida. Ele utiliza o WordNet para encontrar sinônimos de cada
palavra da consulta, e busca entradas no banco de dados cujo conteúdo contenha qualquer um desses termos.

Funções:
- search_database: Conecta-se ao banco de dados, encontra sinônimos para os termos da consulta
  usando WordNet, e retorna as linhas da tabela 'webpages' que contêm esses termos.

Dependências:
- sqlite3: Para operações com o banco de dados SQLite.
- nltk.tokenize.word_tokenize: Para tokenizar a consulta em palavras individuais.
- nltk.corpus.wordnet: Para obter sinônimos de palavras usando WordNet.
"""

import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

def search_database(query):
    """
    Searches the 'webpages' table in an SQLite database for rows containing terms
    related to the input query. The function tokenizes the query, finds synonyms
    for each token using WordNet, and retrieves rows from the database whose 'content'
    column includes any of these terms.

    Args:
        query (str): The search query string to find related terms in the database.

    Returns:
        list: A list of tuples, where each tuple represents a row from the 'webpages'
              table that matches any of the terms or their synonyms from the query.

    How it works:
    - Connects to the SQLite database named 'database.sqlite'.
    - Tokenizes the query string into individual words using NLTK's word_tokenize.
    - For each token, retrieves synonyms (lemmas) using WordNet.
    - Searches for rows in the 'webpages' table where the 'content' column contains
      any of the tokens or their synonyms.
    - Closes the database connection before returning the results.

    Raises:
        sqlite3.Error: If a database error occurs during the connection or query execution.
        LookupError: If required NLTK resources (like WordNet) are not available.
    """

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