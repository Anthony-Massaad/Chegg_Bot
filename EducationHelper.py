import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile, Options


currently_running = False 
# an event is a code that runs when the bot detects a specific activity
chegg_bot = commands.Bot(command_prefix=">")

# On ready event to know when the bot is ready
@chegg_bot.event
async def on_ready():
    print("ready")

# ON message event for the bot commands, rather than using the command prefix
@chegg_bot.event
async def on_message(message):
    """
        Will check if the messages starts with the desired command, and is indeed a chegg link
        Will make sure that it is not already in another user's demand, which is the currently_running boolean
        If not, then the bot will run the check_function method and get the png of the page for that chegg link
        Send it to the user
        If so, unfortunetly, I didn't apply threading for multiple commands so the user needs to wait
    """
    channel = chegg_bot.get_channel("Channel Id as an int")
    global Author
    global currently_running

    if message.content.lower().startswith('!chegg'):
        if message.content.lower().startswith('!chegg https://www.chegg.com'):
            Author = message.author
            if not currently_running:
                currently_running = True
                await channel.send(f'please wait while your link is being processed, {message.author.mention}')
                chegg_function(message.content.split(' ')[1])
                await Author.send(file=discord.File('temp.png'))
                currently_running = False
            else:
                await channel.send(
                    f'Sorry, was processing another link, please try again now, {message.author.mention}')
                currently_running = False

        else:
            await channel.send(f'not a valid chegg link {message.author.mention}')

    await chegg_bot.process_commands(message)

# The function that gets the image of the page for a link
def chegg_function(url):
    """
        Requires the file path of firefox and geckdriver 
        Will open firefox but not visually, access the body of the chegg link, save as pdf called temp
        then exit the driver, meaning exit firefox. 
    """
    FireFoxOptions = FirefoxProfile("FireFox Location path")
    noBrowserOpen = Options()
    noBrowserOpen.headless = True
    driver = webdriver.Firefox(executable_path="geckodriver", options=noBrowserOpen, firefox_profile=FireFoxOptions)
    driver.get(url)
    driver.find_element_by_tag_name('body').screenshot('temp.png')
    driver.quit()

chegg_bot.run("Token")
