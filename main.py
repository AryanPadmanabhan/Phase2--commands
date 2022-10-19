import discord
from discord import app_commands 
import yfinance as yf
import pandas as pd
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=ID)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")


def rvol(stock):
  df = yf.Ticker(stock).history(period='Max')  #gets stock history
  current_volume = df['Volume'][-1]
  avg_volume = df['Volume'].rolling(10).mean()
  avg_volume = avg_volume[-1]
  rvol = current_volume / avg_volume
  return rvol
client = aclient()
tree = app_commands.CommandTree(client)

def get_sq():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  driver.get('https://squeezemetrics.com/monitor/dix')
  screenshot = driver.save_screenshot('14451982418253.png')
  driver.quit()

def get_swaggy():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  driver.get('https://swaggystocks.com/dashboard/wallstreetbets/ticker-sentiment')
  driver.execute_script("window.scrollBy(0,800)","")
  time.sleep(1)
  screenshot = driver.save_screenshot('swaggy.png')
  driver.quit()

def get_twitter():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
  driver.get('https://tradestie.com/apps/twitter/most-active-stocks/')
  time.sleep(1)
  screenshot = driver.save_screenshot('twitter.png')
  driver.quit()

def topvol(stock, choice):
  c = -2
  p = -1
 
  if choice == 'c':
    best_options = {}
    for exp in yf.Ticker(stock).options:

      vol = yf.Ticker(stock).option_chain(exp)[c]['volume']
      strikes = yf.Ticker(stock).option_chain(exp)[c]['strike']
      best_options[exp] = [strikes[max(range(len(vol)), key=vol.__getitem__)], max(vol)]

      keys = list(best_options.keys())
      lst = sorted(keys, key=lambda x: best_options[x][1], reverse=True)
    lst = lst[:5]
    myTable = PrettyTable(["Expiration", "Strike", "Vol"])
    for expiration in lst:
      myTable.add_row([str(expiration), str(best_options[expiration][0]) + 'c', best_options[expiration][1]])
    return myTable

  if choice == 'p':
    best_options = {}
    for exp in yf.Ticker(stock).options:
      vol = yf.Ticker(stock).option_chain(exp)[p]['volume']
      strikes = yf.Ticker(stock).option_chain(exp)[p]['strike']

      best_options[exp] = [strikes[max(range(len(vol)), key=vol.__getitem__)], max(vol)]

      keys = list(best_options.keys())
      lst = sorted(keys, key=lambda x: best_options[x][1], reverse=True)

    
    lst = lst[:5]
    myTable = PrettyTable(["Expiration", "Strike", 'Vol'])
    for expiration in lst:
      myTable.add_row([str(expiration), str(best_options[expiration][0]) + 'p', best_options[expiration][1]])
    return myTable

def get_short_info(stock):

  short_float = yf.Ticker(stock).info['shortPercentOfFloat']
  short_float = short_float * 100

  return short_float


@tree.command(guild = discord.Object(id=ID), name = 'rvol', description='Get the Relative Volume of any stock') #guild specific slash command
async def self(interaction: discord.Interaction, stock: str):
  await interaction.response.defer()
  rvolume = rvol(stock)
  embed = discord.Embed(
    title=f'Relative Vol. of {stock}',
    description=f'```diff\n- Relative Volume {round(rvolume, 2)}```',
    color=discord.Colour.green())
  await interaction.followup.send(embed=embed)

@tree.command(guild = discord.Object(id=ID), name = 'topvol', description='Get the most liquid options of any stock') #guild specific slash command
async def self(interaction: discord.Interaction, stock: str, c_or_p: str):
  await interaction.response.defer()
  options = topvol(stock, c_or_p)
  embed = discord.Embed(
    title=f'Liquid Options',
    description=f'```diff\n+ Most Liquid Options for {stock} \n{options}```',
    color=discord.Colour.green())
  await interaction.followup.send(embed=embed)


@tree.command(guild = discord.Object(id=ID), name = 'sfloat', description='Get the short float of any stock') #guild specific slash command
async def self(interaction: discord.Interaction, stock: str):
  await interaction.response.defer()
  short_float = get_short_info(stock)
  embed = discord.Embed(
    title=f'Short Float',
    description=f'```diff\n+ Short float for {stock}: {round(short_float, 2)}%```',
    color=discord.Colour.green())
  await interaction.followup.send(embed=embed) 

@tree.command(guild = discord.Object(id=ID), name = 'sqme', description='Get the squeeze metrics') #guild specific slash command 
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  get_sq()
  await interaction.followup.send(file = discord.File('14451982418253.png')) 

@tree.command(guild = discord.Object(id=ID), name = 'wsb', description='Get trending stocks on WSB') #guild specific slash command 
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  get_swaggy()
  await interaction.followup.send(file = discord.File('swaggy.png')) 

@tree.command(guild = discord.Object(id=ID), name = 'twitter', description='Get trending stocks on Twitter') #guild specific slash command 
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  get_twitter()
  await interaction.followup.send(file = discord.File('twitter.png')) 

client.run('TOKEN')
