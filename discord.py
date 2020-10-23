
import discord
import time
import asyncio

messages = joined = 0


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time : {int(time.time())}, messages : {messages} , members joined: {joined} \n")
            messages = 0
            joined = 0
            await asyncio.sleep(60)
        except Exception as e:
            print(e)


@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("admin") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="Nope")


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to elio's test server !{member.mention}""")


@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(id)
    friends = ["ElioH#4938", "Sabson#8938", "Killua Zoldyck#0517"]

    badwords = ["idiot", "dumb", "loser"]
    for word in badwords:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("No cursing here !")
    if message.content == "help":
        embed = discord.Embed(title="ElioBot here to assist you in your journey !", description="My command list")
        embed.add_field(name="hello", value="Greets the user")
        embed.add_field(name="users", value="Shows the server's current user number")
        embed.add_field(name="age/old", value="Shows each user's age")
        await message.channel.send(content=None, embed=embed)
    if client.user.id != message.author.id:
        if (message.content.find("old") != -1 or message.content.find("age") != -1) and str(message.author) in friends:
            await message.channel.send("Everyone here is 21 years old !")
        if message.content.find("hello") != -1 or message.content.find("hi") != -1 or message.content.find("hey") != -1:
            await message.channel.send("Hi , I'm ElioBot, here to assist you !")
        if message.content.find("users") != -1:
            await message.channel.send(f"""# of members in this server : {id.member_count}""")
        if message.content.find("how are you") != -1 or message.content.find("sup") != -1:
            await message.channel.send("I'm good how are you ?")
        if message.content == "ez":
            await message.channel.send("peezy lemon squeezy !")
        if message.content.find(":p") != -1:
            await message.channel.send("Emoji user huh ?")
        if message.content.find("thank") != -1 and str(message.author) in friends:
            await message.channel.send("Your wish is my command , master !")
        else:
            await message.channel.send("You are welcome !")
        if message.content.find("bot") != -1:
            await message.channel.send("Who told you I'm a bot ?")
        if message.content == "bye" or message.content == "Bye":
            await message.channel.send("Take care !!")


client.loop.create_task(update_stats())
client.run(token)

