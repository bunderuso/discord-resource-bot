import discord

#defining function to create embeds
def create_embed(user_items, username):
    #getting all keys from user_items
    item_names = user_items.keys()
    embed = discord.Embed(
        title=f"{username}'s inventory")

    for i in item_names:
        if i == "_id":
            continue
        else:
            embed.add_field(name=i, value=user_items[i], inline=False)

    return embed