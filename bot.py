import re
import sqlite3
import requests
from discord.ext.commands import Bot
import discord
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from transformers import pipeline, set_seed
import nltk

from generator import generate_sentence, build_and_train_model, get_data
from crawler_bfs import crawl_bfs

nltk.download('wordnet')

# Initialize the text generation pipeline
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# Constants
BASE_URL = 'https://api.spoonacular.com/'
PATTERN_NUMBER = r"^[0-9]{1,5}$"
PATTERN_FOOD = r'\w+'
API_KEY = '911952be2b1e4b549c6eb2a8ef2e7130'

# Initialize Discord bot client
intents = discord.Intents.all()
client = Bot(command_prefix='!', intents=intents)


@client.command()
async def hello(ctx):
    """Send a greeting message."""
    await ctx.send('Hello, this is the Equal Chatbot in private.')


@client.command()
async def source(ctx):
    """Provide the source code link."""
    await ctx.reply(
        """The link for the source code of the bot is here on GitHub:
        https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py"""
    )


@client.command()
async def author(ctx):
    """Provide the author's email and name."""
    await ctx.reply(
        'The chatbot author email is felipe.nudelman@gmail.com, and his name is Felipe Aron',
        mention_author=True
    )


@client.command()
async def help_(ctx):
    """Provide help information for available commands."""
    help_message = (
        "Here is the help function where we inform the available Equal Chatbot commands.\n"
        "To run a command, you should start your message with `!`.\n"
        "The available commands are:\n"
        "- `hello`: Displays a greeting message from the chatbot.\n"
        "- `source`: Provides a link to the source code of the bot on GitHub.\n"
        "- `author`: Displays information about the chatbot's author.\n"
        "- `get_random_recipes`: Retrieves random recipes for meals.\n"
        "- `get_recipes_with_autocompletion`: Retrieves recipes based on autocompletion.\n\n"
        "To use the `get_random_recipes` command, run: `!get_random_recipes <number>`.\n"
        """Replace `<number>` with
        the desired number of random recipes.\n"""
        """To use the `get_recipes_with_autocompletion` command, run
        : `!get_recipes_with_autocompletion <query>`.\n"""
        "Replace `<query>` with the food or word you want to search for.\n\n"
        "Example usages:\n"
        "- `!get_random_recipes 3`: Retrieves 3 random recipes.\n"
        """- `!get_recipes_with_autocompletion chicken`: 
        Retrieves recipes with autocompletion for the word 'chicken'.\n\n"""
        "We use the Spoonacular API (https://api.spoonacular.com) to retrieve the recipes."
    )
    await ctx.reply(help_message)


@client.command()
async def get_random_recipes(ctx, number: int):
    """Retrieve random recipes based on the provided number."""
    if not 1 <= number <= 5:
        await ctx.reply('The number of recipes is invalid. Please choose a number between 1 and 5.')
        return

    url = f'{BASE_URL}/recipes/random/'
    params = {'number': number, 'apiKey': API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        recipes = [recipe['title'] for recipe in data['recipes']]
        await ctx.reply(f'The random recipes are: {", ".join(recipes)}')
    except requests.RequestException as e:
        print(e)
        await ctx.reply('An error occurred while retrieving random recipes.')


@client.command()
async def get_recipes_with_autocompletion(ctx, query):
    """Retrieve recipes based on autocompletion of the provided query."""
    if not query:
        await ctx.reply('The query for recipes is empty. Please provide a word.')
        return

    if not re.match(PATTERN_FOOD, query):
        await ctx.reply('The query for recipes is invalid. Please provide a valid word.')
        return

    url = f'{BASE_URL}/recipes/autocomplete/'
    params = {'query': query, 'apiKey': API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        recipes = [recipe['title'] for recipe in data]
        await ctx.reply(f'The autocompleted recipes are: {", ".join(recipes)}')
    except requests.RequestException as e:
        print(e)
        await ctx.reply('An error occurred while retrieving autocompleted recipes.')


@client.command()
async def crawl(ctx, url):
    """Perform a breadth-first crawl starting from the provided URL."""
    crawl_queue = await crawl_bfs(url)
    while crawl_queue:
        current_url = crawl_queue.pop(0)
        await ctx.send(f"Crawling {current_url}")
        print(f'Crawling {current_url}')
        crawl_queue.extend(await crawl_bfs(current_url))
    await ctx.send("Crawling finished!")


@client.command()
async def generate(ctx, term):
    """Generate text based on the provided term using a trained model."""
    await ctx.send(f"Generating text for term {term}")
    model, tokenizer, max_sequence_length = build_and_train_model(get_data())
    print(f'Generating text for term {term}')
    generated_text = generate_sentence(term, model, tokenizer, max_sequence_length)
    await ctx.send(f'{term} {generated_text}')


@client.command()
async def generate_gpt(ctx, term):
    """Generate text based on the provided term using the GPT-2 model."""
    await ctx.send(f"Generating text for term {term} using gpt2 model")
    generated = generator(term, max_length=30, num_return_sequences=1)[0]['generated_text']
    print(generated)
    await ctx.send(generated)


@client.command()
async def wn_search(ctx, term, threshold=None):
    """Search for URLs in the database based on similar words in the term."""
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    inverted_index = {}

    if threshold:
        query = "SELECT * FROM webpages WHERE sentiment >= ?"
        rows = c.execute(query, (threshold,))
    else:
        rows = c.execute("SELECT * FROM webpages")

    for row in rows:
        url, content = row[1], row[2]
        tokens = word_tokenize(content.lower())
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = set()
            inverted_index[token].add(url)

    similar_words = set()
    tokens = word_tokenize(term.lower())
    for synset in wordnet.synsets(term):
        for lemma in synset.lemmas():
            similar_words.add(lemma.name())

    results = set()
    for similar_word in similar_words:
        if similar_word in inverted_index:
            results.update(inverted_index[similar_word])

    results = list(results)
    query = "SELECT * FROM webpages WHERE url IN ({})".format(', '.join('?' for _ in results))
    c.execute(query, results)
    rows = c.fetchall()
    conn.close()

    await ctx.send(results)


@client.command()
async def search(ctx, term, threshold=None):
    """Search for webpages in the database based on 
    the provided term and optional sentiment threshold."""
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    if threshold:
        query = "SELECT * FROM webpages WHERE sentiment >= ?"
        rows = c.execute(query, (threshold,))
    else:
        rows = c.execute("SELECT * FROM webpages")

    results = []
    for row in rows:
        url, content = row[1], row[2]
        if term.lower() in content.lower():
            results.append(url)

    conn.close()
    await ctx.send(results)


if __name__ == "__main__":
    client.run('YOUR_DISCORD_BOT_TOKEN')
