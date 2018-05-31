#CoHBot
#By DracoRanger
import asyncio
import random
from collections import deque
import discord
from discord.ext import commands


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
with open(cardBlack) as b:#I NEED A QUEUE!
    black = deque(random.shuffle(b.readlines()))
with open(cardsWhite) as w:
    white = deque(random.shuffle(w.readlines()))



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
    global playersGotten
    if message.author == client.user:
        return
    if message.channel == client.get_channel(channelNum):
        '''
        plays game
        '''
        if message.content.startswith('!startGame') and not gameStarted:
            temp = "Ok, game is starting.\nAnyone who wants to play reply with !in.\nSomeone responsible type !done."
            gameStarted = True
            playersGotten = False
            await client.send_message(message.channel, temp)
        elif message.content.startswith('!in') and gameStarted:
            if message.author not in players:
                players.append(message.author)
        elif message.content.startswith('!done') and gameStarted:
            playersGotten = True
            for i in players:
                hand = []
                for j in range(0, 7):
                    card = black.pop()
                    hand.append(black[j])
                    black.append(card)
                cardStorage.append(hand)
            for i in range(0, len(players)):
                await client.send_message(players[i], cardStorage[i])
        elif message.content.startswith('!deal') and playersGotten:
            for i in range(0, len(players)):
                if i == currentDealer:
                    await client.send_message(players[i], "Choose the best!")
                    wCard = white.pop()
                    white.append(wCard)
                    await client.send_message(message.channel, wCard)
            currentDealer = currentDealer + 1
            if currentDealer == len(players):
                currentDealer = 0
        elif message.content.startswith('!choose') and playersGotten:
            if int(message.content[8:-1]) >= 0 and int(message.content[8:-1]) <= 5:
                locl = players.index(message.author)
                await client.send_message(message.channel, cardStorage[locl][int(message.content[8:-1])])
                del cardStorage[locl][int(message.content[8:-1])]
                card = black.pop()
                cardStorage[locl].append(card)
                black.append(card)


        '''
        prints all commands
        '''
        if message.content.startswith('!help'):
            keylistDaily = "**!startGame** = "
            keylistWeekly = "**!in** = "
            gib = "**!done** = "
            takeDaily = "**!deal** = "
            takeWeekly = "**!choose** = "

            ret = keylistDaily+'\n'+takeDaily+'\n\n'+keylistWeekly+'\n'+takeWeekly+'\n\n'+gib+'\n'
            await client.send_message(message.channel, ret)

client.run(token)
