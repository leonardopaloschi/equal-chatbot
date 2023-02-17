import discord

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!hello':
            await message.channel.send('Hello, this is the Equal Chatbot in private.')

        if message.content.startswith('!source'):
            await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py!', mention_author=False)

        if message.content.startswith('!author'):
            await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)
    else:
        if message.content.lower() == '!hello':
            await message.channel.send('Hello, this is the Equal Chatbot in public!')

        if message.content.startswith('!source'):
            await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py!', mention_author=False)

        if message.content.startswith('!author'):
            await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)

client.run('')