#keyBot
#By DracoRanger
import asyncio
import random
import discord
from discord.ext import commands
#import logging

client = discord.Client()
bot = commands.Bot(command_prefix="!", description="")

BOT_FOLDER = ""

config = open('botData.txt', 'r')
conf = config.readlines() #push to array or do directly
token = conf[0][:-1]
cardsBlack = conf[1][:-1]
cardsWhite = conf[2][:-1]
channelNum = conf[3][:-1]

gameStarted = False
playersGotten = False
players = []
cardStorage = []
currentDealer = 0

black = ''
white = ''
with open cardsBlack as b:#I NEED A QUEUE!
    black = b.readlines().randomize()
with open cardsWhite as w:
    white = w.readlines().randomize()



@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    #print(client.user.id)
    print('------')
    message = client.user.name + " is prepared to ruin childhoods."
    await client.send_message(client.get_channel(channelNum), message)

@client.event
@asyncio.coroutine
async def on_message(message):
    global channelNum
    global gameStarted
    global players
    global black
    global white
    global cardStorage
    global currentDealer
    if message.author == client.user:
        return
    if message.channel == client.get_channel(channelNum):
        '''
        plays game
        '''
        if message.content.startswith('!startGame') and not gameStarted:
            temp = "Ok, game is starting.\nAnyone who wants to play reply with !in.\nSomeone responsible type !done."
            gameStarted = not gameStarted
            await client.send_message(message.channel, temp)
        elif message.content.startswith('!in') and gameStarted:
            if message.author not in players:
                players.append(message.author)
        elif message.content.startswith('!done') and gameStarted:
            playersGotten = True
            init = 0
            for i in players:
                hand = []
                for j in range(init, init + 5):
                    hand.append(black[j])
                cardStorage.append(hand)
            for i in range(0, len(player)):
                await client.send_message(player[i],cardStorage[i])
        elif message.content.startswith('!deal') and playersGotten:
            for i in range(0, len(player)):
                if i == currentDealer:
                    await client.send_message(player[i],"Choose the best!")
                    await client.send_message(message.channel, white.next())
            currentDealer = currentDealer + 1
        elif message.content.startswith('!choose') and playersGotten:
            if int(message.content[7:-1])>=0 and int(message.content[7:-1])<=5:
                message.author location in players
                await client.send_message(message.channel, cardStorage[i][int(message.content[7:-1])])
                cardStorage[i][int(message.content[7:-1])] remove
                cardStorage[i].append(black.next())


        '''
        prints all commands
        '''
        if message.content.startswith('!help'):
            keylistDaily = "**!keysDaily** = prints a list of the daily games, works in either server or in pms"
            keylistWeekly = "**!keysWeekly** = prints a list of the weekly games, works in either server or in pms"
            gib = "**!gib [gameName] [key]**= gives a key to the bot, only works in pms"
            takeDaily = "**!takeDaily [gameName]** = messages you with the game's key, works only in server, recieve key in pm, message posted to server"
            takeWeekly = "**!takeWeekly [gameName]** = messages you with the game's key, works only in server, recieve key in pm, message posted to server"

            ret = keylistDaily+'\n'+takeDaily+'\n\n'+keylistWeekly+'\n'+takeWeekly+'\n\n'+gib+'\n'
            await client.send_message(message.channel, ret)

client.run(token)
