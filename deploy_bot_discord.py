import discord

client = discord.Client()

@client.event
async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')

@client.event
async def on_message(self, message):
    # we do not want the bot to reply to itself
    if message.author.id == self.user.id:
        return

    if message.content.startswith('!source'):
        await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py!', mention_author=True)

    if message.content.startswith('!author'):
        await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)

client.run('')