import discord
import re
import requests
import json

intents = discord.Intents.all()

base_url = 'https://api.spoonacular.com/'
pattern_number = r"^[0-9]{1,5}$"
pattern_food = '\w+'

api_key = '911952be2b1e4b549c6eb2a8ef2e7130'

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!hello':
            await message.channel.send('Hello, this is the Equal Chatbot in private.')

        if message.content.startswith('!source'):
            await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py')

        if message.content.startswith('!author'):
            await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)

        if message.content.startswith('!help'):
            await message.reply('Here is the help function where we inform the available Equal Chatbot commands.\nTo run a command you should start your message with !. \nThe avaiblable commands are hello, source, author, get_random_recipes and get_recipes_with_autocompletion. \nTo run !source, !help and !author you just need to type it and the bot should return a help, in the case of !help, just to check if the bot is online, the source code of the bot in case of !source and the github of the author in case of !author. \nThe command get_random_recipes is used to check the for random possible recipes you can do for your meal. \nThe command get_recipes_with_autocompletion is used to check for recipes with autocompletion.\nTo use the first command you should run something like !run get_random_recipes 3. This means you are looking for 3 random recipes in the bot.\nThe get_recipes_with_autocompletion is used inputing a word/food you like. You can use it with !run get_recipes_with_autocompletion chicken. It should return to you meals with chicken \nWe use the https://api.spoonacular.com to retrieve to you the recipes.')

        if message.content.startswith('!run'):
            message_splited = message.content.split(' ')
            if len(message_splited) != 3:
                await message.reply('You did not provided the correct number of arguments. 3 are necessary.')
            else:
                if message_splited[1] == 'get_random_recipes':
                    if message_splited[2]:
                        if re.match(pattern_number, message_splited[2]):
                            url = base_url + '/recipes/random/'
                            params={'number': message_splited[2], 'apiKey': api_key}
                            try:
                                response = requests.get(url, params=params)    
                            except Exception as e:
                                print(e)
                            response = json.loads(response.text)
                            string_chatbot = ''
                            for i in range(0, len(response['recipes'])):
                                string_chatbot = string_chatbot + response['recipes'][i]['title']
                                if i != len(response['recipes']) - 1:
                                    string_chatbot = string_chatbot + ', '
                            await message.reply('The random recipes are here ' + string_chatbot + '.')
                        else:
                            await message.reply('The number of recipes ' + message_splited[2] + ' is invalid. Minimum 1 and maximum 5')
                    else:
                        await message.reply('You did not provided a number of recipes you want')

                elif message_splited[1] == 'get_recipes_with_autocompletion':
                    if message_splited[2]:
                        if re.match(pattern_food, message_splited[2]):
                            url = base_url + '/recipes/autocomplete/'
                            params={'query': message_splited[2], 'apiKey': api_key}
                            try:
                                response = requests.get(url, params=params)    
                            except Exception as e:
                                print(e)
                            response = json.loads(response.text)
                            string_chatbot = ''
                            for i in range(0, len(response)):
                                string_chatbot = string_chatbot + response[i]['title']
                                if i != len(response) - 1:
                                    string_chatbot = string_chatbot + ', '

                            await message.reply('The autocompleted recipes are here ' + string_chatbot + '.')
                        else:
                            await message.reply('The query of recipes ' + message_splited[2] + ' is invalid. Not a word')
                    else:
                        await message.reply('You did not provided a number of recipes you want')

                else:
                    await message.reply('Second parameter of the !run command is invalid please use the ones listed in !help')

    else:
        if message.content.lower() == '!hello':
            await message.channel.send('Hello, this is the Equal Chatbot in private.')

        if message.content.startswith('!source'):
            await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py')

        if message.content.startswith('!author'):
            await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)

        if message.content.startswith('!help'):
            await message.reply('Here is the help function where we inform the available Equal Chatbot commands.\nTo run a command you should start your message with !. \nThe avaiblable commands are hello, source, author, get_random_recipes and get_recipes_with_autocompletion. \nTo run !source, !help and !author you just need to type it and the bot should return a help, in the case of !help, just to check if the bot is online, the source code of the bot in case of !source and the github of the author in case of !author. \nThe command get_random_recipes is used to check the for random possible recipes you can do for your meal. \nThe command get_recipes_with_autocompletion is used to check for recipes with autocompletion.\nTo use the first command you should run something like !run get_random_recipes 3. This means you are looking for 3 random recipes in the bot.\nThe get_recipes_with_autocompletion is used inputing a word/food you like. You can use it with !run get_recipes_with_autocompletion chicken. It should return to you meals with chicken \nWe use the https://api.spoonacular.com to retrieve to you the recipes.')

        if message.content.startswith('!run'):
            message_splited = message.content.split(' ')
            if len(message_splited) != 3:
                await message.reply('You did not provided the correct number of arguments. 3 are necessary.')
            else:
                if message_splited[1] == 'get_random_recipes':
                    if message_splited[2]:
                        if re.match(pattern_number, message_splited[2]):
                            url = base_url + '/recipes/random/'
                            params={'number': message_splited[2], 'apiKey': api_key}
                            try:
                                response = requests.get(url, params=params)    
                            except Exception as e:
                                print(e)
                            response = json.loads(response.text)
                            string_chatbot = ''
                            for i in range(0, len(response['recipes'])):
                                string_chatbot = string_chatbot + response['recipes'][i]['title']
                                if i != len(response['recipes']) - 1:
                                    string_chatbot = string_chatbot + ', '

                            await message.reply('The random recipes are here ' + string_chatbot + '.')
                        else:
                            await message.reply('The number of recipes ' + message_splited[2] + ' is invalid. Minimum 1 and maximum 5')
                    else:
                        await message.reply('You did not provided a number of recipes you want')

                elif message_splited[1] == 'get_recipes_with_autocompletion':
                    if message_splited[2]:
                        if re.match(pattern_food, message_splited[2]):
                            url = base_url + '/recipes/autocomplete/'
                            params={'query': message_splited[2], 'apiKey': api_key}
                            try:
                                response = requests.get(url, params=params)    
                            except Exception as e:
                                print(e)
                            
                            response = json.loads(response.text)
                            string_chatbot = ''
                            for i in range(0, len(response)):
                                string_chatbot = string_chatbot + response[i]['title']
                                if i != len(response) - 1:
                                    string_chatbot = string_chatbot + ', '

                            await message.reply('The autocompleted recipes are here ' + string_chatbot + '.')
                        else:
                            await message.reply('The query of recipes ' + message_splited[2] + ' is invalid. Not a word')
                    else:
                        await message.reply('You did not provided a number of recipes you want')

                else:
                    await message.reply('Second parameter of the !run command is invalid please use the ones listed in !help')

client.run('MTA3NTUyOTk3NzA5MDU0NzcyMw.GzGHgL.gTyJkuSyBsQv9gUTNZe4IS2ZPX_I4CMJlxB_I4')