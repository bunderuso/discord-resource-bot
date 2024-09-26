# bot.py
import os
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands
import mongo_funcs
import message_formatter

client = mongo_funcs.connect_mongo()



load_dotenv()

#defining the intents
intents = discord.Intents.all()

#reading the token from the secret file
token_file = open("token_file.txt", "r")
token = token_file.readlines()
TOKEN = token[0].strip()

#defining the bot command prefix
bot = commands.Bot(command_prefix='$', intents=intents)

#turning on the bot
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


#test command
@bot.command(name='99')
async def beans(ctx):
    print("in beans")
    response = "I like beans"
    await ctx.send(response)

#writing to the mongo
@bot.command(name='add_resource')
async def add_resource(ctx, username, *args):
    print("in add_resource")

    #getting the member
    user = await bot.fetch_user(int(username.strip("<@!>")))

    #confirming the member exists
    if user:
        #getting current resources of user or adding new entry
        user_items = mongo_funcs.user_check(client=client, user_id=user.id)

        #adding new user items
        for i in range(len(args)):
            #print(args[i])
            #getting the name and qty  of resources
            split_str = str(args[i]).split(":")

            #checking if items exists in the inventory already
            if split_str[0] in user_items.keys():
                user_items[split_str[0]] += int(split_str[1])
            else:
                user_items[split_str[0]] = int(split_str[1])

        print(user_items)
        #updating the inventory
        mongo_funcs.update_inventory(client=client, user_id=user.id, inv_struct=user_items)


        await ctx.send(f"User ID of {user.name} is {user.id}")
    else:
        await ctx.send("No user found with that name")

#getting the current items of a user
@bot.command(name='show_user_resources')
async def show_resources(ctx, *args):
    print("in show_resources")
    # getting the member
    user = await bot.fetch_user(int(args[0].strip("<@!>")))
    if user:
        user_items = mongo_funcs.user_check(client=client, user_id=int(user.id))

        #creating the embedded message
        embedded_mess = message_formatter.create_embed(user_items, user.name)
        await ctx.send(embed=embedded_mess)
    else:
        await ctx.send("No user found with that name")

bot.run(TOKEN)