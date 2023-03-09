#til alt
import discord
from discord.ext import commands
#til tictactoe
import random

#til hangman
import random
import string
#hangman module eget
from hangmanord import ord


#generelle bot settings
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")



@bot.command()
async def help(ctx): #kunne ha lagd dette mye bedre, men gadd ikke og hadde ikke tid.
    embed = discord.Embed( 
        color=discord.Color.orange(),
        description="Her får ligger kommand listen til Gigabot:",
    )
    embed.set_author(name="Help")
    embed.add_field(name="!games", value="Viser alle spill du kan spille.", inline=True)
    embed.add_field(name="!tictactoe", value="Tictactoe spill. !tictactoe for å starte spillet (@ to spillere. Første @ starter.), !place for å plassere (+ 1 - 9) ", inline=True)
    embed.add_field(name="!hangman, !place", value="Hangman spill. !hangman for å starte spillet (husk å @ hvem som spiller.), !L for å velge bokstaver.", inline=True)
    embed.add_field(name="!8ball", value="Kast en 8 ball som svarer et valgfritt spørsmål, på engelsk. Husk å skrive noe etter !8ball. ", inline=True)
    embed.add_field(name="!skaper", value="GI KOMPLEMENTER TIL DEN ALLMEKTIGE SKAPEREN IVER. IKKE SKRIV NEGATIVE TING. HUSK Å SKRIVE ET ADJEKTIV ETTER KOMMANDEN.", inline=True)
    embed.add_field(name="!ola", value="En liten credit kommand til Ola, siden han er en tulling.", inline=True)
    embed.add_field(name="!gif", value="Random (ish) gif.", inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def games(ctx):
    embed=discord.Embed(title="GAMES/SPILL", url="https://en.wikipedia.org/wiki/Game", description="!tictactoe, !hangman", color=0x06440F)
    embed.add_field(name="!tictactoe", value="Tictactoe med 2 spillere.", inline=True)
    embed.add_field(name="!hangman", value="Hangman med 1 spiller.", inline=True)
    await ctx.send(embed=embed)



# 8ball 

@bot.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it",
                "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                "Don’t count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
    await ctx.send(f"Spørsmål: {question}\n8ball svar: {random.choice(responses)}")
# tictactoe 
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []
boardAfter = [False, False, False,
              False, False, False,
              False, False, False]



winningConditions = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [8,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,8]
]


@bot.command()
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count
    print("hello")
    if gameOver:
        print("hello2")
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
        ]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2
        print(player1, player2)

        #print board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += "" + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += "" + board[x]

        #hvem først
        num = 1
        if num == 1:
            turn = player1
            await ctx.send("Din tur, <@" + str(player1.id) + ">.")
        if num == 2:
            turn = player2
            await ctx.send("Din tur, <@" + str(player2.id) + ">.")

    else: 
        await ctx.send("Et spill blir fortsatt spilt. Spill det ferdig før dere starter nytt.")
    

@bot.command()
async def place(ctx, pos : int):
    global turn 
    global player1
    global player2
    global board
    global boardAfter
    global count
    

    if not gameOver:
        mark = ""
        
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            print(pos)
            if 0 < pos < 10 and board[pos - 1]:
                board[pos - 1] = mark
                count += 1

                #print brett
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += "" + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += "" + board[x]
                if turn == player1:
                    await ctx.send("Din tur, <@" + str(player1.id) + ">.")
                elif turn == player2: 
                    await ctx.send("Din tur, <@" + str(player2.id) + ">.")
                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send(mark + " vant!")
                elif count >= 9:
                    await ctx.send("Det ble uavgjort!")
                
                #bytte person som spiller
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else: 
                await ctx.send("Husk å velge et heltall mellom 1 og 9 og en ubrukt del av brettet.")
        else: 
            await ctx.send("Det er ikke din tur.")
    else:
        await ctx.send("Start et nytt spill, med bruk av !tictactoe kommanden.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] and board[condition[2]] == mark:
            gameOver = True

#tictactoe error handling
@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Vennligst velg to spillere for denne kommanden.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Vennligst husk å pinge/mention spillere (f.eks. <@1079681151989469284>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Vennligst velg en posisjon du vil ha brikken din plassert.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Vennligst husk å skriv inn et heltall (f.eks. 0, 1, 2 osv.).")
#tictactoe slutt


#hangman
word = ""
lives = 0
hangmanRunning = False
currentPlayer = ""
word_letters = ""
used_letter = ""
alphabet = ""
word_state = "_" * len(word)
hangmanpics = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']
hangmanpics.reverse()


def get_valid_word(words):
    word = random.choice(words)
    while "-" in words or " " in words:
        word = random.choice(words)
    return word


@bot.command()
async def hangman(ctx, player: discord.Member):
    global currentPlayer
    global lives
    global word
    global word_letters
    global used_letter
    global hangmanRunning
    global alphabet
    global word_state

    currentPlayer = player
    lives = 6
    word = get_valid_word(ord)
    word_letters = set(word) # bokstavene i ordet
    alphabet = set(string.ascii_lowercase)
    used_letter = set() #hvilke ord som har blitt brukt
    hangmanRunning = True
    print(word)
    
    while hangmanRunning and currentPlayer == ctx.author:
        if currentPlayer == ctx.author:
            if len(word_letters) > 0 and lives > 0:
                await ctx.send("Velg bokstav:")
                bokstav = await bot.wait_for("message", check = lambda message: message.author == ctx.author)
                user_letter = str(bokstav.content)
                print(user_letter)


                
                if user_letter in alphabet - used_letter:
                    used_letter.add(user_letter)
                    if user_letter in word_letters:
                        word_letters.remove(user_letter)
                    else:
                        lives = lives - 1
                        await ctx.send("Bokstaven din er ikke i ordet.")
                    await ctx.send(hangmanpics[lives])
                elif user_letter in used_letter:
                    await ctx.send("Du har allerede brukt den bokstaven")
                
                user_letter.join(used_letter)
                used_letter_string = ""
                
                for i in used_letter:
                    used_letter_string = used_letter_string + i + ", "
                await ctx.send("Du har " + str(lives) + " liv igjen og du har brukt disse bokstavene: " + used_letter_string) 

                word_list = [letter if letter in used_letter else "-" for letter in word]
                await ctx.send("Nåværende ord: " + " ".join(word_list))

            elif lives == 0:
                await ctx.send(f"Du døde, ordet var {word}. Bedre lykke neste gang.")
            else: 
                await ctx.send(f"Du gjettet ordet {word}!")
                hangman = False
                return
        else:
            await ctx.send("Ikke din tur.")

#hangman error handling
@hangman.error
async def hangmanError():
    await ctx.send("Vennligst husk å skrive inn hvem som spiller etter kommanden. (f.eks. !letter b)")


#diverse commands
@bot.command()
async def ola(ctx):
    await ctx.send("ola er en liten tulling")

@bot.command()
async def skaper(ctx, kompliment):
    negative = ["stygg", "rar", "lav", "ukul", "upen"]
    if kompliment in negative:
        await ctx.send("IVER ER IKKE " + kompliment)
    else:
        await ctx.send("Skaperen min er Iver. Iver er " + kompliment + ".")
@skaper.error
async def skaperError():
    await ctx.send("Vennligst husk et kompliment om Iver.")


RickRoll =  ["https://tenor.com/view/things-that-you-shouldnt-stare-at-for-too-long-the-sun-winnie-the-pooh-rickroll-rick-astley-gif-16585085","https://tenor.com/view/rickroll-rick-roll-rickastley-spongebob-gif-19367765", "https://tenor.com/bn826.gif", "https://tenor.com/biqXZ.gif"]

@bot.command()
async def gif(ctx):
  await ctx.send(random.choice(RickRoll))

# for at botten skal runne. bruker bot token som er laget på discord side.
bot.run("MTA3OTY4MTE1MTk4OTQ2OTI4NA.GzQHiI.dqVyKx54q2On7YXbU_cr8z1uws4o70dsTmw6kM")
