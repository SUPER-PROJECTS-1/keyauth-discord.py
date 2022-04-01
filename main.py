'''
        Keyauth Discord Bot, made in discord.py made by Super™#9999
        Thanks to keyauth for making this possible > keyauth.win
        Any help DM me on discord and we can sort this out!
        All this was possible by keyauth.docs

        1. Install the modules using discord.py (pip install ...)
        2. Go to config setup your keyauth and tokens
        3. The run the bot!
        4. You are free to customize and share this product as long as you leave credits here.
'''

# Will need to install most of these (pip install ... | Example: pip install discord.py)
from http.client import FORBIDDEN
from logging import PlaceHolder
from msilib.schema import Component
from turtle import color
from discord import embeds
from discord.ext import commands
import discord
from discord.ext.commands.core import has_permissions
from discord.ext.commands.core import has_role
from discord.ext.commands import CommandNotFound
from discord.ext.commands.errors import CommandInvokeError, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, CommandNotFound, NoPrivateMessage
import string
import random
from discord.ext import tasks
import datetime
import requests
from requests import *
import json
from discord.ext import commands
from discord.utils import get
from discord.ui import Button, View
from discord.ext import commands
from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONFIG 

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.AutoShardedBot(command_prefix='!', intents=intents)
bot.remove_command('help')


KEYAUTHLICENSE = "" # Can be found in seller settings in your keyauth.win dashboard
STATUS = "keyauth.win" # The bots status
DOWNLOAD = "" # The download to your program
OWNERID = "" # Enter your discord ID
token = "" # Your bot token can be found at discord developers portal

# https://htmlcolorcodes.com/color-picker/
DefaultColour = discord.Colour(0x242424) 
AuthColour = discord.Colour(0xd9d9d9) 
SuccessColour = discord.Colour(0x2fad09) 
ErrorColour = discord.Colour(0xad0909) 

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# RUNNING/ERRORS

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    activity = discord.Game(name=STATUS)
    await bot.change_presence(status=discord.Status.online, activity=activity)
  
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        cooldown = discord.Embed(title="Cooldown!", description=f"{ctx.author.mention}, This command is on cooldown!", colour=ErrorColour) 
        cooldown.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=cooldown) 

    if isinstance(error, MissingPermissions):
        MissinPermissions = discord.Embed(title="Perms!", description=f"{ctx.author.mention}, This bot is missing permissions!", colour=ErrorColour) 
        MissinPermissions.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=MissinPermissions) 

    if isinstance(error, MissingRequiredArgument):
        Argument = discord.Embed(title="Command Usage!", description=f"{ctx.author.mention}, You are not using this command correctly!", colour=ErrorColour) 
        Argument.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=Argument) 

    if isinstance(error, CommandNotFound):
        NotFound = discord.Embed(title="Command Failure!", description=f"{ctx.author.mention}, Unknown commands you can do ``>help`` for all commands!", colour=ErrorColour) 
        NotFound.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=NotFound) 

    if isinstance(error, NoPrivateMessage):
        PrivateMessage = discord.Embed(title="Command Failure!", description=f"{ctx.author.mention}, This command cannot be used in ``DM``", colour=ErrorColour) 
        PrivateMessage.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=PrivateMessage) 

    if isinstance(error, CommandOnCooldown):
        PrivateMessage = discord.Embed(title="Command Failure!", description=f"{ctx.author.mention}, This command is on ``cooldown``", colour=ErrorColour) 
        PrivateMessage.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=PrivateMessage) 

    if isinstance(error, CommandInvokeError):
        NotFound = discord.Embed(title="Unkown Error!", description=f"{ctx.author.mention}, Uncaptured error. (Check console for more information)", colour=ErrorColour) 
        NotFound.set_footer(text=f"USER: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=NotFound) 
        print(error)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# HELP SYSTEM
# How it works: The user runs the command and it sends all the available commands.

@bot.command(name="commands")
async def _commands(ctx):
        embed = discord.Embed(colour=DefaultColour)   
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        embed.add_field(name = "Generation Commands", value=f"``genweek <amount>`` ``genmonth <amount>`` ``genlife <amount>``", inline=False) 
        embed.add_field(name = "Keyauth Commands", value=f"``reset <username> <reason>`` ``deletelicense <key>`` ``deleteuser <user>`` ``extend <username> <sub> <days>`` ``blacklistip <ip>`` ``banaccount <user> <reason>`` ``unbanaccount <user>`` ``claim <license>`` ``keywipe`` ``killsessions`` ``license <license>`` ``user <user>`` ``resetpass <user> <new-password>`` ``authstatus`` ``download`` ``allsubscriptions``", inline=False) 
        embed.set_footer(text=f"<> = Required Argument", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=embed)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GENERATION SYSTEM
# How it works: The user who executes the command will be checked if ID is matched in Generation-perms.json if so will send a license to the users DM. 

@bot.command()
async def generateweek(ctx, amount):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=add&expiry=7&mask=xxxxxxxxxxxxxxxxxxxxxxxxxxx&level=1&amount={amount}&format=text" 
        response = requests.get(url)
        embed = discord.Embed(title=f"Keyauth - ({amount}) Weekly Subscription Keys Generated!", description="```\n%s```" % (response.text), colour=AuthColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.author.send(embed=embed)

        embed = discord.Embed(title="Keyauth - Keys Generated!", description=f"{ctx.author.mention}, We sent you ``{amount}`` of ``weekly_subscripton`` via your DM!", colour=AuthColour) 
        await ctx.send(embed=embed) 

@bot.command()
async def generatemonth(ctx, amount):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=add&expiry=31&mask=xxxxxxxxxxxxxxxxxxxxxxxxxxx&level=2&amount={amount}&format=text"
        response = requests.get(url)
        embed = discord.Embed(title=f"Keyauth - ({amount}) Monthly Subscription Keys Generated!", description="```\n%s```" % (response.text), colour=AuthColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.author.send(embed=embed)

        embed = discord.Embed(title="Keyauth - Keys Generated!", description=f"{ctx.author.mention}, We sent you ``{amount}`` of ``monthly_subscripton`` via your DM!", colour=AuthColour) 
        await ctx.send(embed=embed) 

@bot.command()
async def generatelife(ctx, amount):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=add&expiry=9999&mask=xxxxxxxxxxxxxxxxxxxxxxxxxxx&level=4&amount={amount}&format=text"
        response = requests.get(url)
        embed = discord.Embed(title=f"Keyauth - ({amount}) Lifetime Subscription Keys Generated!", description="```\n%s```" % (response.text), colour=AuthColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.author.send(embed=embed)

        embed = discord.Embed(title="Keyauth - Keys Generated!", description=f"{ctx.author.mention}, We sent you ``{amount}`` of ``lifetime_subscripton`` via your DM!", colour=AuthColour) 
        await ctx.send(embed=embed)  

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STATS SYSTEM
# How it works: Returns all users / all subscriptions or how many licenses in use etc...

@bot.command()
async def stats(ctx):
    url = f'https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=fetchallusernames&format=text'
    r = requests.get(url, allow_redirects=True)
    open('users.txt', 'wb').write(r.content)

    url2 = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=stats&format=json"
    response2 = requests.get(url2)
    sds = response2.json()
    UNUSED = sds["unused"]

    with open("users.txt", 'r') as fp:
        x = len(fp.readlines())

        embed = discord.Embed(title="Keyauth - Statistics", description=f"**All Customers:** ``{x}``\n**Unused Licenses:** ``{UNUSED}``", colour=AuthColour)  
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")

        await ctx.send(embed=embed)
        
@bot.command()
async def allsubscriptions(ctx):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
            url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=fetchallsubs"
            response = requests.get(url)
            sds = response.json()
            SUB1 = sds["subs"][0]["name"]
            SUB2 = sds["subs"][1]["name"]
            SUB3 = sds["subs"][2]["name"]
            SUB4 = sds["subs"][4]["name"]

            embed = discord.Embed(title="Keyauth - All Subscriptions", description=f"```Here is every single subscription in the database.``` \n> ``{SUB1}``\n> ``{SUB2}``\n> ``{SUB3}``\n> ``{SUB4}``", colour=AuthColour)  
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
            await ctx.send(embed=embed)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BASIC COMMANDS
# How it works: Auth status, just returns keyauth's website ping etc. | Download can download your program!

@bot.command()
async def authstatus(ctx):
    response = requests.get('https://keyauth.win/')

    url2 = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=getsettings&format=json"
    response2 = requests.get(url2)
    sds = response2.json()
    STAT = sds["enabled"]
    embed = discord.Embed(title="Keyauth Auth Status", description=f"**Website Response:** ``{response.status_code} : ✅``\n**Response Time:** ``{response.elapsed.total_seconds()}``\n**Application Status:** ``✅ {STAT}``", colour=AuthColour)  
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
    await ctx.send(embed=embed)

@bot.command()
async def download(ctx):
         embed = discord.Embed(title="Keyauth Keyauth Download:", description=f"```Version: 1.0.0```", color=DefaultColour)
         embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
         embed.add_field(name="Download:", value=f"||{DOWNLOAD}||", inline=False)
         await ctx.author.send(embed=embed)
         
         embed = discord.Embed(title="Download sent to DM!", description=f"{ctx.author.mention}, We sent the download link to your ``DM!`` \n\n> Discord: https://discord.gg/WveHU8kN2h \n> Shop: https://Keyauthstore.tebex.io/", colour=SuccessColour) 
         embed.set_footer(text=f"Customer: {ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
         await ctx.send(embed=embed) 

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ACCOUNT CREATION
# How it works: The users does !claim license and it will return a user and password so they can login! (The user + password are randomly generated strings)

@bot.command()
async def claim(ctx, key):

        user = string.ascii_uppercase
        passw = string.ascii_uppercase

        username = (''.join(random.choice(user) for i in range(7)))
        password = (''.join(random.choice(passw) for i in range(5)))
        
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=activate&user={username}&key={key}&pass={password}&format=text"
        response = requests.get(url)
        test = response.json()
        SUB = test["message"]
        if SUB == "Logged in!":
            embed = discord.Embed(title="Keyauth - Account Created", color=AuthColour)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
            embed.add_field(name="Username:", value=f"``{username}``", inline=True)
            embed.add_field(name="Password:", value=f"``{password}``", inline=True)
            embed.add_field(name="License:", value=f"``{key}``", inline=True)
            embed.add_field(name="Claimed ID:", value=f"``{ctx.author} : {ctx.author.id}``", inline=True)
            await ctx.author.send(embed=embed)     

            successmsg = discord.Embed(title="", description = f"**License has been claimed! Check DM For Details.**", color=SuccessColour)
            successmsg.add_field(name="Information:", value=f"{ctx.author} has became a customer! ``[{key}]``")
            successmsg.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
            await ctx.send(embed=successmsg)   

        if SUB == "Key Not Found.":
            embed = discord.Embed(title="Account Creation Failed!", description = f"```License is not found, make sure you use correct license!```" , color=0xfc0303)
            await ctx.author.send(embed=embed) 

            errorrrr = discord.Embed(title="Account creation failure!", description = f"> License is invalid, sent information to (DM) [{ctx.author.mention}]", color=0xfc0303)
            await ctx.send(embed=errorrrr)

        if SUB == "Key Already Used.":
            embed = discord.Embed(title="Account Creation Failed!", description = f"```License is already used, make sure you use correct license!```" , color=0xfc0303)
            await ctx.author.send(embed=embed) 

            errorrrr = discord.Embed(title="Account Creation Failed!", description = f"> License is invalid, sent information to (DM) [{ctx.author.mention}]", color=0xfc0303)
            await ctx.send(embed=errorrrr)     

        if SUB == "Username Already Exists.":  
            embed = discord.Embed(title="Account Creation Failed!", description = f"```Username already taken, re-attempt this please!```" , color=0xfc0303)
            await ctx.author.send(embed=embed) 

            errorrrr = discord.Embed(title="Account Creation Failed!", description = f"> Creation failure, sent information to (DM) [{ctx.author.mention}]", color=0xfc0303)
            await ctx.send(embed=errorrrr) 

        if SUB == "Your license is banned.":  
            embed = discord.Embed(title="Account Creation Failed!", description = f"```This license key is banned, contact support team!```" , color=0xfc0303)
            await ctx.author.send(embed=embed) 

            errorrrr = discord.Embed(title="Account Creation Failed!", description = f"> Creation failure, sent information to (DM) [{ctx.author.mention}]", color=0xfc0303)
            await ctx.send(embed=errorrrr)   

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# HARDWARE RESET
# How it works: Resets a users HWID, so they can share the application with a friend / login onced resetted there PC.

@bot.command()
async def hwidreset(ctx, username, *, reason):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=resetuser&user={username}&format=json"
        response = requests.get(url)
        test = response.json()
        SUB = test["message"]
        if SUB == "Successfully reset user!":
            embed = discord.Embed(title = "Reset Completed!", description=f"> Reset for user ``{username}`` was reset for reason ``{reason}``", colour=AuthColour)  
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
            embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
            await ctx.send(embed=embed)  

        else:

            embed = discord.Embed(title = "Reset Failed!", description=f"> Reset for user ``{username}`` failed! ``(This can be due to user is already reset or username invalid)``", colour=ErrorColour)  
            embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
            await ctx.send(embed=embed)  

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LICENSE INFORMATION
# How it works: Gathers the users key status/username/creation date and returns

@bot.command()
async def license(ctx, KEY):
    try:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=info&key={KEY}&format=text"
        response = requests.get(url)
        sds = response.json()
        STATUS = sds["status"]
        USER = sds["usedby"]
        CREATED =sds["creationdate"]
        embed = discord.Embed(title="Subscription Was Found!", color=AuthColour)
        embed.add_field(name="License:", value=f"``{KEY}``", inline=False)
        embed.add_field(name="Username:", value=f"``{USER}``", inline=False)
        embed.add_field(name="Status:", value=f"``{STATUS}``", inline=False)
        embed.add_field(name="License Created:", value=f"``{CREATED}``", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="Subscription Not Returned", color=ErrorColour)
        embed.add_field(name="License:", value=f"``{KEY}``", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USER INFORMATION
# How it works: Gathers the users subscription/expiry + hwid/ip + creation date + last login date and then gathers there IP information this is dangerous to use in public chats!

@bot.command()
async def user(ctx, USER):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        try:
            url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=userdata&user={USER}&format=text"
            response = requests.get(url)
            sds = response.json()
            SUB = sds["subscriptions"][0]["subscription"]
            EXPIRY = sds["subscriptions"][0]["expiry"]
            HWID = sds["hwid"]
            IP = sds["ip"]
            CREATION = sds["createdate"]
            LAST = sds["lastlogin"]

            url2 = f"http://ip-api.com/json/{IP}"
            response2 = requests.get(url2)
            apple = response2.json()
            COUNTRY = apple["country"]
            COUNTRYCODE = apple["countryCode"]
            CITY = apple["city"]
            TIMAEZONE = apple["timezone"]
            ZIPC = apple["zip"]
            REGION = apple["regionName"]
            REGIONID = apple["region"]

            PROV = apple["isp"]

            embed = discord.Embed(title="Subscription Was Found!", color=AuthColour)
            embed.add_field(name="Username:", value=f"``{USER}``", inline=False)
            embed.add_field(name="Subscription:", value=f"``{SUB}``", inline=False)
            embed.add_field(name="Expiration:", value=f"``" + datetime.utcfromtimestamp(int(EXPIRY)).strftime('%Y-%m-%d %H:%M:%S') + "``", inline=False)
            embed.add_field(name="HWID Binded:", value=f"``{HWID}``", inline=False)
            embed.add_field(name="IP Binded:", value=f"||{IP}|| ```🌎 Country : {COUNTRY} [{COUNTRYCODE}]\n🌎 Region : {REGION} [{REGIONID}]\n🌎 City : {CITY}\n⏰ Timezone : {TIMAEZONE}\n📞 Internet Provider: {PROV}```", inline=False)
            embed.add_field(name="Last Login:", value=f"``" + datetime.utcfromtimestamp(int(LAST)).strftime('%Y-%m-%d %H:%M:%S') + "``", inline=False)
            embed.add_field(name="User Created:", value=f"``" + datetime.utcfromtimestamp(int(CREATION)).strftime('%Y-%m-%d %H:%M:%S') + "``", inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
            await ctx.send(embed=embed)
        except:
             embed = discord.Embed(title="Subscription Not Returned", color=ErrorColour)
             embed.add_field(name="Username:", value=f"``{USER}``", inline=False)
             embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
             await ctx.send(embed=embed)                      

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USER MANAGEMENT
# How it works: Delete/Extend/Password/Blacklist/Sessions/Ban/Unban

@bot.command()
async def deletelicense(ctx, key):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=del&key={key}&format=text"
        response = requests.get(url)
    if response.text == "Successfully Deleted License":
        response = requests.get(url)
        keydelete = discord.Embed(title = "License Deleted!", description=f"> License key ``{key}`` was deleted from database. This request was from {ctx.author.mention}", colour=AuthColour)  
        keydelete.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=keydelete)
    else:
        licensedelfail = discord.Embed(title = "License Delete Failed!", description=f"> License key ``{key}`` was not found in database, we cannot delete. This request was from {ctx.author.mention}", colour=ErrorColour)  
        licensedelfail.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=licensedelfail)

@bot.command()
async def deleteuser(ctx, *, username):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=deluser&user={username}&format=text"
        response = requests.get(url)
    if response.text == "Successfully deleted user!":
        keydelete = discord.Embed(title = "User Deleted!", description=f"> Client ``{username}`` was deleted from database. This request was from {ctx.author.mention}", colour=AuthColour)  
        keydelete.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=keydelete)
    else:
        licensedelfail = discord.Embed(title = "User Delete Failed!", description=f"> Client ``{username}`` was not found in database, we cannot delete. This request was from {ctx.author.mention}", colour=ErrorColour)  
        licensedelfail.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=licensedelfail)

@bot.command()
async def keywipe(ctx):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=delunused&format=text"
        response = requests.get(url)
        keydelete = discord.Embed(title = "Key Wipe!", description=f"> All ``unused`` licenses was wiped from datatbase. This request was from {ctx.author.mention}", colour=AuthColour)  
        keydelete.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=keydelete)

@bot.command()
async def killsessions(ctx):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Error!", description="You cant do that either because you are not the owner of the application", colour=DefaultColour) 
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=killall"
        response = requests.get(url)
        keydelete = discord.Embed(title = "Killed all sessions!", description=f"> All users logged into the application have been logged out or suspended.", colour=AuthColour)  
        keydelete.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        keydelete.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=keydelete)

@bot.command()
async def extend(ctx, username, sub, days):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=extend&user={username}&sub={sub}&expiry={days}&format=text"
        response = requests.get(url)
        embed = discord.Embed(title="User Extended", description="%s" % (response.text), colour=AuthColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)

@bot.command()
async def blacklistip(ctx, ip):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=black&ip={ip}&format=text"
        response = requests.get(url)
        embed = discord.Embed(title="Blacklist", description="%s" % (response.text), colour=AuthColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        
@bot.command()
async def resetpass(ctx, user, *, password):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=resetpw&user={user}&passwd={password}&format=json"
        response = requests.get(url)
        test = response.json()
        SUB = test["message"]
    if SUB == "Password reset successful":
        embed = discord.Embed(title="Account Password Resetted!", description=f"> Client ``{user}`` password has been reset to ``{password}`` This request was from {ctx.author.mention}", colour=AuthColour) 
        embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Password Reset Failed!", description=f"> Client ``{user}`` was not found in database, we cannot reset password from Keyauth.cc! This request was from {ctx.author.mention}", colour=ErrorColour) 
        embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=embed)

@bot.command()
async def banaccount(ctx, key, *, reason):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=banuser&user={key}&reason={reason}&format=json"
        response = requests.get(url)
        test = response.json()
        SUB = test["message"]
    if SUB == "Successfully banned user!":
        embed = discord.Embed(title="Keyauth Account Banned!", description=f"> Client ``{key}`` has been ``permantly`` banned from Keyauth.cc! With reason ``{reason}``. This request was from {ctx.author.mention}", colour=AuthColour) 
        embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Keyauth Account Banned Failure!", description=f"> Client ``{key}`` was not found in database, we cannot ban from Keyauth.cc! This request was from {ctx.author.mention}", colour=ErrorColour) 
        embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=embed)

@bot.command()
async def unbanaccount(ctx, user):
    if ctx.author.id != (OWNERID):  
        embed = discord.Embed(title="Keyauth - Invalid Permissions!", description=f"[{ctx.author.mention}], You do not have access to execute this command!", colour=ErrorColour) 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
        return
    else:
        url = f"https://keyauth.win/api/seller/?sellerkey={KEYAUTHLICENSE}&type=unbanuser&user={user}&format=text"
        response = requests.get(url)
        test = response.json()
        SUB = test["message"]
    if SUB == "Successfully unbanned user!":
        embed = discord.Embed(title="Keyauth Account Unbanned!", description=f"> Client ``{user}`` has been ``unbanned``. This request was from {ctx.author.mention}", colour=AuthColour) 
        embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Keyauth Account Unbanned Failure!", description=f"> Client ``{user}`` was not found in database, we cannot ban from Keyauth.cc! This request was from {ctx.author.mention}", colour=ErrorColour) 
        embed.set_footer(text=f"{ctx.author}", icon_url="https://cdn.discordapp.com/attachments/949785989574967366/958824078230323200/74461371.png") 
        await ctx.send(embed=embed)


bot.run(token)