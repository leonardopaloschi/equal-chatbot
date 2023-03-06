import discord
import re
import requests
import json

intents = discord.Intents.all()

base_url = 'https://api3.binance.com'
pattern = r"^[a-zA-Z][-a-zA-Z0-9]*[A-Z]{2,}$"

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!hello':
            await message.channel.send('Hello, this is the Equal Chatbot in private.')

        if message.content.startswith('!source'):
            await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py!')

        if message.content.startswith('!author'):
            await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)

        if message.content.startswith('!help'):
            await message.reply('Here is the help function where we inform the available Equal Chatbot commands.\nTo run a command you should start your message with !run. \nThe avaiblable commands are check_symbol_average_price_last_five_minutes and check_symbol_last_trade_price_and_quantity. \nThe command check_symbol_average_price_last_five_minutes is used to check the value of the average price of a currency related to other currency. \nThe command check_symbol_last_trade_price_and_quantity is used to check the value and the quantity of the last trade in certain currency related to other.\nTo use this commands you should use the first currency, you want to know the price or the price and the quantity of the last, and then the other like BTCUSDT, without any bar or hyphen. \nAn example is: !run check_symbol_last_trade_price_and_quantity BTCUSDT. \nWe use the Binance API which is located here https://api3.binance.com to inform the values')

        if message.content.startswith('!run'):
            message_splited = message.content.split(' ')
            if len(message_splited) != 3:
                await message.reply('You did not provided the correct number of arguments. 3 are necessary.')
            else:
                if message_splited[1] == 'check_symbol_average_price_last_five_minutes':
                    if message_splited[2]:
                        if re.match(pattern, message_splited[2]):
                            url = base_url + '/api/v3/avgPrice'
                            params={'symbol': message_splited[2]}
                            response = requests.get(url, params=params)
                            response = json.loads(response.text)
                            await message.reply('The value of the symbol ' + message_splited[2] + ' equals to ' + response['price'] + '.')
                        else:
                            await message.reply('The symbol ' + message_splited[2] + ' is invalid')
                    else:
                        await message.reply('You did not provided a symbol')
                elif message_splited[1] == 'check_symbol_last_trade_price_and_quantity':
                    if message_splited[2]:
                        if re.match(pattern, message_splited[2]):
                            url = base_url + '/api/v3/trades'
                            params={'symbol': message_splited[2]}
                            response = requests.get(url, params=params)
                            response = json.loads(response.text)
                            await message.reply('Symbol ' +  message_splited[2] + ' last trade price was ' + response[0]['price'] + ' and the quantity was ' + response[0]['qty'] + '.')
                        else:
                            await message.reply('The symbol ' + message_splited[2] + ' is invalid')
                    else:
                        await message.reply('You did not provided a symbol')

                else:
                    await message.reply('Second parameter of the !run command is invalid please use the ones listed in !help')

    else:
        if message.content.lower() == '!hello':
            await message.channel.send('Hello, this is the Equal Chatbot in public!')

        if message.content.startswith('!source'):
            await message.reply('The link for the source code of the bot is here in Github: https://github.com/aronfelipe/equal-chatbot/blob/main/deploy_bot_discord.py!')

        if message.content.startswith('!author'):
            await message.reply('The chatbot author email is: felipe.nudelman@gmail.com and his name is Felipe Aron', mention_author=True)

        if message.content.startswith('!help'):
            await message.reply('Here is the help function where we inform the available Equal Chatbot commands.\nTo run a command you should start your message with !run. \nThe avaiblable commands are check_symbol_average_price_last_five_minutes and check_symbol_last_trade_price_and_quantity. \nThe command check_symbol_average_price_last_five_minutes is used to check the value of the average price of a currency related to other currency. \nThe command check_symbol_last_trade_price_and_quantity is used to check the value and the quantity of the last trade in certain currency related to other.\nTo use this commands you should use the first currency, you want to know the price or the price and the quantity of the last, and then the other like BTCUSDT, without any bar or hyphen. \nAn example is: !run check_symbol_last_trade_price_and_quantity BTCUSDT. \nWe use the Binance API which is located here https://api3.binance.com to inform the values')

        if message.content.startswith('!run'):
            message_splited = message.content.split(' ')
            if len(message_splited) != 3:
                await message.reply('You did not provided the correct number of arguments. 3 are necessary.')
            else:
                if message_splited[1] == 'check_symbol_average_price_last_five_minutes':
                    if message_splited[2]:
                        if re.match(pattern, message_splited[2]):
                            url = base_url + '/api/v3/avgPrice'
                            params={'symbol': message_splited[2]}
                            response = requests.get(url, params=params)
                            response = json.loads(response.text)
                            await message.reply('The value of the symbol ' + message_splited[2] + ' equals to ' + response['price'] + '.')
                        else:
                            await message.reply('The symbol ' + message_splited[2] + ' is invalid')
                    else:
                        await message.reply('You did not provided a symbol')
                elif message_splited[1] == 'check_symbol_last_trade_price_and_quantity':
                    if message_splited[2]:
                        if re.match(pattern, message_splited[2]):
                            url = base_url + '/api/v3/trades'
                            params={'symbol': message_splited[2]}
                            response = requests.get(url, params=params)
                            response = json.loads(response.text)
                            await message.reply('Symbol ' +  message_splited[2] + ' last trade price was ' + response[0]['price'] + ' and the quantity was ' + response[0]['qty'] + '.')
                        else:
                            await message.reply('The symbol ' + message_splited[2] + ' is invalid')
                    else:
                        await message.reply('You did not provided a symbol')

                else:
                    await message.reply('Second parameter of the !run command is invalid please use the ones listed in !help')

client.run('')