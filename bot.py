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
with open(cardsBlack) as b:#I NEED A QUEUE!
    temp = b.readlines()
    random.shuffle(temp)
    black = deque(temp)
with open(cardsWhite) as w:
    temp = w.readlines()
    random.shuffle(temp)
    white = deque(temp)



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
            stor = "Ok, game is starting.\nAnyone who wants to play reply with !in.\nSomeone responsible type !done."
            gameStarted = True
            playersGotten = False
            await client.send_message(message.channel, stor)
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
                car = ''
                num = 0
                for j in cardStorage[i]:
                    car = car + str(num)+': ' + j
                    num = num + 1
                await client.send_message(players[i], car)
        elif message.content.startswith('!deal') and playersGotten:
            for i in range(0, len(players)):
                if i == currentDealer:
                    await client.send_message(players[i], "Choose the winner")
                    wCard = white.pop()
                    await client.send_message(message.channel, wCard)
                    white.append(wCard)
                else:
                    await client.send_message(players[i], "Select your card")
        elif message.content.startswith('!selectWinner') and players[currentDealer] == message.author:
            await client.send_message(players[int(message.content[14])], "Good choice!\nYou won the round!")
            for i in range(0, len(players)):
                car = ''
                num = 0
                for j in cardStorage[i]:
                    car = car + str(num)+': ' + j
                    num = num + 1
                await client.send_message(players[i], car)
            currentDealer = currentDealer + 1
            if currentDealer == len(players):
                currentDealer = 0
        elif message.content.startswith('!clear'):
            gameStarted = False
            playersGotten = False
            players = []
            cardStorage = []
            currentDealer = 0
            await client.send_message(message.channel, "Cleared")
        elif message.content.startswith('!help'):
            start_game = "**!startGame** = Begins the game"
            join_in = "**!in** = join game"
            finished = "**!done** = everyone who wants has joined"
            deal = "**!deal** = distribute a black card"
            select = "**!choose** + int = player selects a card from their hand, posts it to the main chat, so do it in a private channel"
            winner = "**!selectWinner** + int = Chooser selects a winner"
            clear = "**!clear** = ends the game and gets it ready for the next game"
            ret = start_game+'\n'+join_in+'\n\n'+finished+'\n'+deal+'\n\n'+select+'\n'+winner+'\n\n'+clear
            await client.send_message(message.channel, ret)

    if message.content.startswith('!choose') and playersGotten and message.channel.is_private:
        #implement error checking
        if int(message.content[8]) >= 0 and int(message.content[8]) <= 6:
            locl = players.index(message.author)
            await client.send_message(client.get_channel(channelNum), str(locl)+': '+cardStorage[locl][int(message.content[8])])
            del cardStorage[locl][int(message.content[8])]
            card = black.pop()
            cardStorage[locl].append(card)
            black.append(card)

client.run(token)
