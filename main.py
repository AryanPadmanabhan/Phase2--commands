import discord
from discord import app_commands 
import yfinance as yf
import pandas as pd
from prettytable import PrettyTable

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=[INSERT ID HERE])) #guild specific: leave blank if global (global registration can take 1-24 hours)
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




@tree.command(guild = discord.Object(id=[INSERT ID HERE]), name = 'rvol', description='Get the Relative Volume of any stock') #guild specific slash command
async def self(interaction: discord.Interaction, stock: str, con: str):
  rvolume = rvol(stock)
  embed = discord.Embed(
    title=f'rVol of {stock}',
    description=f'```diff\n- Relative Volume {round(rvolume, 2)}```',
    color=discord.Colour.green())
  await interaction.response.send_message(embed=embed)

@tree.command(guild = discord.Object(id=[INSERT ID HERE]), name = 'topvol', description='Get the most liquid options of any stock') #guild specific slash command
async def self(interaction: discord.Interaction, stock: str, contract: str):
  options = topvol(stock, contract)
  embed = discord.Embed(
    title=f'Liquid Options',
    description=f'```diff\n+ Most Liquid Options for {stock} \n{options}```',
    color=discord.Colour.green())
  await interaction.channel.send(embed=embed) 

client.run(INSERT AUTH CODE)
