import discord
import re
import requests
import json
import sqlite3
from discord.ext.commands import Bot
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

import nltk

from generator import generate_sentence, train_model

from crawler_bfs import crawl_bfs
nltk.download('wordnet')

intents = discord.Intents.all()

from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

base_url = 'https://api.spoonacular.com/'
pattern_number = r"^[0-9]{1,5}$"
pattern_food = '\w+'

api_key = '911952be2b1e4b549c6eb2a8ef2e7130'

client = Bot('!', intents=intents)

@client.command()
async def hello(ctx):
    await ctx.send('Hello, this is the Equal Chatbot in private.')  # Send a greeting message to the context (ctx)

@client.command()
async def source(ctx):
    await ctx.reply('The link for the source code of the bot is here on GitHub: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py')  # Send a reply with the link to the source code on GitHub

@client.command()
async def author(ctx):
    await ctx.reply('The chatbot author email is felipe.nudelman@gmail.com, and his name is Felipe Aron', mention_author=True)  # Send a reply with information about the chatbot author, mentioning the author's name
    
@client.command()
async def help_(ctx):
    # Help message providing information about the available commands and their usage
    help_message = """Here is the help function where we inform the available Equal Chatbot commands.
    To run a command, you should start your message with `!`.
    The available commands are:
    - `hello`: Displays a greeting message from the chatbot.
    - `source`: Provides a link to the source code of the bot on GitHub.
    - `author`: Displays information about the chatbot's author.
    - `get_random_recipes`: Retrieves random recipes for meals.
    - `get_recipes_with_autocompletion`: Retrieves recipes based on autocompletion.
    
    To use the `get_random_recipes` command, run: `!get_random_recipes <number>`. Replace `<number>` with the desired number of random recipes.
    To use the `get_recipes_with_autocompletion` command, run: `!get_recipes_with_autocompletion <query>`. Replace `<query>` with the food or word you want to search for.
    
    Example usages:
    - `!get_random_recipes 3`: Retrieves 3 random recipes.
    - `!get_recipes_with_autocompletion chicken`: Retrieves recipes with autocompletion for the word "chicken".
    
    We use the Spoonacular API (https://api.spoonacular.com) to retrieve the recipes."""
    
    await ctx.reply(help_message)  # Send the help message as a reply to the context (ctx)

@client.command()
async def get_random_recipes(ctx, number: int):
    if number < 1 or number > 5:
        await ctx.reply('The number of recipes is invalid. Please choose a number between 1 and 5.')  # If the number is not within the valid range
        return  # Exit the function
    url = base_url + '/recipes/random/'  # Construct the URL for retrieving random recipes
    params = {'number': number, 'apiKey': api_key}  # Set the number and API key as parameters for the request
    try:
        response = requests.get(url, params=params)  # Send a GET request to the API endpoint with the parameters
        response = json.loads(response.text)  # Parse the response as JSON

        recipes = [recipe['title'] for recipe in response['recipes']]  # Extract the titles of the recipes from the response
        await ctx.reply('The random recipes are: {}'.format(', '.join(recipes)))  # Send a reply with the random recipe titles
    except Exception as e:
        print(e)  # Print the exception to the console for debugging purposes
        await ctx.reply('An error occurred while retrieving random recipes.')  # Send an error message if an exception occurs

@client.command()
async def get_recipes_with_autocompletion(ctx, query):
    if not query:
        await ctx.reply('The query for recipes is empty. Please provide a word.')  # If the query is empty
        return  # Exit the function
    if not re.match(pattern_food, query):
        await ctx.reply('The query for recipes is invalid. Please provide a valid word.')  # If the query doesn't match the pattern
        return  # Exit the function
    url = base_url + '/recipes/autocomplete/'  # Construct the URL for autocompleted recipes
    params = {'query': query, 'apiKey': api_key}  # Set the query and API key as parameters for the request
    try:
        response = requests.get(url, params=params)  # Send a GET request to the API endpoint with the query and API key
        response = json.loads(response.text)  # Parse the response as JSON
        recipes = [recipe['title'] for recipe in response]  # Extract the titles of the recipes from the response
        await ctx.reply('The autocompleted recipes are: {}'.format(', '.join(recipes)))  # Send a message with the autocompleted recipes
    except Exception as e:
        print(e)  # Print the exception to the console for debugging purposes
        await ctx.reply('An error occurred while retrieving autocompleted recipes.')  # Send an error message if an exception occurs

@client.command()
async def crawl(ctx, url):
    crawl_queue = await crawl_bfs(url)  # Invoke a breadth-first crawl function and get the initial crawl queue
    while crawl_queue:
        await ctx.send("Crawling " + crawl_queue[0])  # Send a message indicating the URL being crawled
        print('Crawling ' + crawl_queue[0])  # Print the URL being crawled
        await crawl_bfs(crawl_queue.pop(0))  # Pop the first URL from the crawl queue and invoke the crawl function on it
    await ctx.send("Crawling finished!")  # Send a message indicating the completion of crawling

@client.command()
async def generate(ctx, term):
    await ctx.send("Generating text for term " + term)  # Send a message indicating the term for which text is being generated
    model, tokenizer, max_sequence_length = train_model() # Train the model and get the tokenizer and maximum sequence length
    print('Generating text for term ' + term) # Print the term for which text is being generated
    await ctx.send(term + ' '+ generate_sentence(term, model, tokenizer, max_sequence_length))  # Send a message indicating the completion of text generation

@client.command()
async def generate_gpt(ctx, term):
    await ctx.send("Generating text for term " + term +  " using gpt2 model")  # Send a message indicating the term for which text is being generated
    print(generator(term, max_length=30, num_return_sequences=1))
    await ctx.send(generator(term, max_length=30, num_return_sequences=1)[0]['generated_text'])  # Send a message indicating the term for which text is being generated

@client.command()
async def wn_search(ctx, term, threshold=None):
    conn = sqlite3.connect('database.sqlite')  # Connect to the SQLite database
    c = conn.cursor()  # Create a cursor object to execute SQL queries
    inverted_index = {}  # Initialize an empty dictionary for the inverted index
    if threshold:
        rows = c.execute("SELECT * FROM webpages WHERE sentiment >= " + threshold + ';')
    else:
        rows = c.execute("SELECT * FROM webpages;") # Execute a SQL query to fetch all rows from the 'webpages' table
    for row in rows:
        url, content = row[1], row[2]  # Extract the URL and content from the row
        tokens = word_tokenize(content.lower())  # Tokenize the content and convert it to lowercase
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = set()  # Create an empty set for each unique token
            inverted_index[token].add(url)  # Add the URL to the set associated with the token
    similar_words = set()  # Initialize an empty set to store similar words
    tokens = word_tokenize(term.lower())  # Tokenize the search term and convert it to lowercase
    for synset in wordnet.synsets(term):  # Iterate over synsets (word senses) of the search term in WordNet
        for lemma in synset.lemmas():  # Iterate over the lemmas (variants) of each synset
            similar_words.add(lemma.name())  # Add the lemma (similar word) to the set of similar words
    results = set()  # Initialize an empty set to store the search results
    for similar_word in similar_words:
        if similar_word in inverted_index:
            results = results.union(inverted_index[similar_word])  # Add the URLs associated with each similar word to the results set
    results = list(results)  # Convert the results set to a list
    # Execute a SQL query to fetch the complete results from the 'webpages' table using the URLs in the results list
    c.execute("SELECT * FROM webpages WHERE url IN ({});".format(', '.join('?' for _ in results)), results)
    rows = c.fetchall()  # Fetch all the rows returned by the query
    conn.close()  # Close the database connection
    await ctx.send(results)  # Send the results (URLs) as a response in the Discord channel

@client.command()
async def search(ctx, term, threshold=None):

    conn = sqlite3.connect('database.sqlite')  # Connect to the SQLite database
    c = conn.cursor()  # Create a cursor object to execute SQL queries

    if threshold:
        rows = c.execute("SELECT * FROM webpages WHERE sentiment >= " + threshold + ';')
    else:
        rows = c.execute("SELECT * FROM webpages;") # Execute a SQL query to fetch all rows from the 'webpages' table

    inverted_index = {}  # Initialize an empty dictionary for the inverted index

    for row in rows:
        url, content = row[1], row[2]  # Extract the URL and content from the row
        tokens = word_tokenize(content.lower())  # Tokenize the content and convert it to lowercase
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = set()  # Create an empty set for each unique token
            inverted_index[token].add(url)  # Add the URL to the set associated with the token

    tokens = word_tokenize(term.lower())  # Tokenize the search term and convert it to lowercase
    results = set()  # Initialize an empty set to store the search results

    for token in tokens:
        if token in inverted_index:
            results = results.union(inverted_index[token])  # Add the URLs associated with each token to the results set

    # Recuperar os resultados completos a partir do banco de dados
    results = list(results)  # Convert the results set to a list
    # Execute a SQL query to fetch the complete results from the 'webpages' table using the URLs in the results list
    c.execute("SELECT * FROM webpages WHERE url IN ({});".format(', '.join('?' for _ in results)), results)
    rows = c.fetchall()  # Fetch all the rows returned by the query
    conn.close()  # Close the database connection
    await ctx.send(results)  # Send the results (URLs) as a response in the Discord channel

client.run('')