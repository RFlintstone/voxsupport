import discord
client = discord.Client()
from discord.ext import commands

print('Loaded Discord.PY')

import datetime
print('Loaded Datetime.')

import asyncio
print('Loaded asyncio.')

import config
print('Loaded Configuration.')

import uuid
print('Loaded UUID.')

import language
print('Loaded Language File (EN).')

import json
print('Loaded JSON.')

import shutil
print('Loaded Shutil.')

from pathlib import Path

print('Loaded Pathlib.')

import os.path

print('Loaded OS Path.')


# -------------------------------------------------------------- #
#                                                                #
# Main Code                                                      #
#                                                                #
# -------------------------------------------------------------- #

def getDefaultSetting(setting):
    with open('servers/default.json', 'r') as jsonfile2:
        data2 = jsonfile2.read().replace('\n', '')

    server = json.loads(data2)

    return server[setting]

def getSetting(guild, setting):
    guild_id = str(guild.id)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    server_file = Path(f"{BASE_DIR}\Discord_Bot\servers\{guild_id}.json")

    if server_file.is_file():

        with open('servers/' + str(guild_id) + '.json', 'r') as jsonfile:
            data = jsonfile.read().replace('\n', '')

        server = json.loads(data)

        return server[setting]

    else:

        with open('servers/default.json', 'r') as jsonfile2:
            data2 = jsonfile2.read().replace('\n', '')

        server = json.loads(data2)

        return server[setting]


def getAllSettings(guild):
    guild_id = str(guild.id)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    server_file = Path(f"{BASE_DIR}\Discord_Bot\servers\{guild_id}.json")

    if server_file.is_file():

        with open('servers/' + str(guild_id) + '.json', 'r') as jsonfile:
            data = jsonfile.read().replace('\n', '')

        return json.loads(data)

    else:

        with open('servers/default.json', 'r') as jsonfile2:
            data2 = jsonfile2.read().replace('\n', '')

        return json.loads(data2)


def setFooter(ctx, embed):
    embed.set_footer(text=f"{language.footer_executed} {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)


async def logger(msg):

    if " " in msg.content:
        cmd = msg.content.split(" ")[0]
    else:
        cmd = msg.content

    msg2 = discord.Embed(title=f"{language.logs_title}", color=0x15A1EE, timestamp=datetime.datetime.utcnow())
    msg2.add_field(name=f"{language.logs_user}", value=f'<@{msg.author.id}>', inline=True)
    msg2.add_field(name=f"{language.logs_user_id}", value=msg.author.id, inline=True)
    msg2.add_field(name=f"{language.logs_channel}", value=f'{msg.channel.mention}\n *({msg.channel.name})*', inline=True)
    msg2.add_field(name=f"{language.logs_command}", value=f'`{cmd}`', inline=True)
    msg2.set_thumbnail(url=msg.author.avatar_url)
    setFooter(msg, msg2)

    admin_logs = int(getSetting(msg.guild, 'admin_logs'))

    await client.get_channel(admin_logs).send(embed=msg2)

    print(f'{language.logs_success_command} ({msg.author.name}) [{msg.author.id }] | {cmd}')


@client.event
async def on_message(message):

    guild = message.guild

    if message.author == client.user:
        return

    server_prefix = getSetting(guild, 'prefix')
    if getSetting(guild, 'admin_logs') is None:
        server_admin_logs = None
    else:
        server_admin_logs = getSetting(guild, 'admin_logs')

    if getSetting(guild, 'verify-channel') is None:
        server_verify_channel = None
    else:
        server_verify_channel = int(getSetting(guild, 'verify-channel'))

    server_verify_role = getSetting(guild, 'verify-role')

    if getSetting(guild, 'ticket-category') is None:
        server_ticket_category = None
    else:
        server_ticket_category = getSetting(guild, 'ticket-category')

    #--------------------------#
    #                          #
    #      About Command       #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'about'):
        embed = discord.Embed(title=f"{language.about_title}", color=0x15A1EE, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f"{language.about_bot_id}", value=client.user.id, inline=True)
        embed.add_field(name=f"{language.about_bot_name}", value=client.user.name , inline=True)
        embed.add_field(name=f"{language.about_version}", value=config.version, inline=True)
        embed.set_thumbnail(url=client.user.avatar_url)
        setFooter(message, embed)
        await message.channel.send(embed=embed)


        await logger(message)

    #--------------------------#
    #                          #
    #      Verify Command      #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'verify'):

        if message.channel.id == server_verify_channel:

            user = message.author

            role = discord.utils.get(user.guild.roles, name=server_verify_role)

            await message.author.add_roles(role)

            embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
            embed.add_field(name=f"Verified!", value="You have verified successfully!", inline=True)
            embed.set_thumbnail(url=client.user.avatar_url)
            setFooter(user, embed)

            await message.channel.send(embed=embed)

            await message.delete(message)


        else:
            return

        await logger(message)

    #--------------------------#
    #                          #
    #      Settings Command    #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'settings'):

        if discord.abc.GuildChannel.permissions_for(message.channel, member=message.author).administrator:

            args = message.content.split()

            if len(message.content.split()) == 1:

                embed = discord.Embed(title=f"{message.guild.name}'s Settings", color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=f"Prefix", value=f"`{server_prefix}`", inline=True)
                embed.add_field(name=f"Admin Logs", value=f"`{server_admin_logs}`", inline=True)
                embed.add_field(name=f"Verify Channel", value=f"`{server_verify_channel}`", inline=True)
                embed.add_field(name=f"Verify Role", value=f"`{server_verify_role}`", inline=True)
                embed.add_field(name=f"Ticket Category", value=f"`{server_ticket_category}`", inline=True)
                embed.set_thumbnail(url=client.user.avatar_url)
                setFooter(message, embed)
                await message.channel.send(embed=embed)

            elif len(message.content.split()) > 2:

                if args[1] in getAllSettings(guild):

                    if args[2] == "set" or args[2] == "Set":

                        if len(message.content.split()) == 4:

                            value = getAllSettings(guild)
                            value[args[1]] = args[3]

                            with open("servers/" + str(guild.id) + ".json", "w") as newdata:

                                json.dump(value, newdata)

                            new_arg = args[3]
                            embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name=f"Set!", value=f"You set the setting {args[1]} to {new_arg}", inline=True)
                            embed.set_thumbnail(url=client.user.avatar_url)
                            setFooter(message, embed)
                            await message.channel.send(embed=embed)

                        else:
                            embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name=f"Error!", value=f"Please enter a value!", inline=True)
                            embed.set_thumbnail(url=client.user.avatar_url)
                            setFooter(message, embed)
                            await message.channel.send(embed=embed)

                    elif args[2] == "reset" or args[2] == "Reset":

                        value = getAllSettings(guild)
                        value[args[1]] = getDefaultSetting(args[1])

                        with open("servers/" + str(guild.id) + ".json", "w") as newdata:

                            json.dump(value, newdata)

                        new_prefix = value[args[1]]
                        embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                        embed.add_field(name=f"Set!", value=f"You set the setting {args[1]} to {new_prefix}", inline=True)
                        embed.set_thumbnail(url=client.user.avatar_url)
                        setFooter(message, embed)
                        await message.channel.send(embed=embed)

                    elif args[2] == " ":

                        embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                        embed.add_field(name=f"Error!", value=f"Please enter more than one arg.", inline=True)
                        embed.set_thumbnail(url=client.user.avatar_url)
                        setFooter(message, embed)
                        await message.channel.send(embed=embed)

                else:

                    embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name=f"Error!", value=f"That setting does not exist!", inline=True)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    setFooter(message, embed)
                    await message.channel.send(embed=embed)
        else:

                    embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name=f"Error!", value=f"You do not have permissions!", inline=True)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    setFooter(message, embed)
                    await message.channel.send(embed=embed)


        await logger(message)

    #--------------------------#
    #                          #
    #      Help Command        #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'help'):
        embed = discord.Embed(title=f"{config.name} {language.help_title}", color=0x15A1EE, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f"{language.help_first_field}", value=f"{language.help_first_value}", inline=True)
        embed.add_field(name=f"{language.help_second_field}", value=f"{language.help_second_value}", inline=True)
        embed.add_field(name=f"{language.help_third_field}", value=f"{language.help_third_value}", inline=True)
        embed.set_thumbnail(url=client.user.avatar_url)
        setFooter(message, embed)
        await message.channel.send(embed=embed)

        await logger(message)

    #--------------------------#
    #                          #
    #     BotInfo Command      #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'botinfo'):
        embed = discord.Embed(title=f"{config.name} Information", color=0x15A1EE, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f"Bot Name", value=f"{client.user.name}", inline=True)
        embed.add_field(name=f"Bot ID", value=f"{client.user.id}", inline=True)
        print(client.guilds.count())
        embed.add_field(name=f"Total Servers", value=f"", inline=True)
        embed.add_field(name=f"Total Members", value=f"", inline=True)
        embed.set_thumbnail(url=client.user.avatar_url)
        setFooter(message, embed)
        await message.channel.send(embed=embed)

        await logger(message)

    #--------------------------#
    #                          #
    #      Userinfo Command    #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'userinfo'):

        try:

            arg = message.content.split()[1]

            embed = discord.Embed(title=f'{message.mentions[0].name}#{message.mentions[0].discriminator} {language.userinfo_title}', color=0x15A1EE, timestamp=datetime.datetime.utcnow())

            embed.add_field(name=f"{language.userinfo_username}", value=f'{message.mentions[0].name}', inline=True)



            embed.add_field(name=f"{language.userinfo_id}", value=f'{message.mentions[0].id}', inline=True)
            created_at = message.mentions[0].created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')

            embed.add_field(name=f"{language.userinfo_creation_date}", value=f'{created_at}', inline=True)
            join_date = message.mentions[0].joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')

            embed.add_field(name=f"{language.userinfo_join_date}", value=f'{join_date}', inline=True)
            activity = message.mentions[0].activity

            if activity is None:
                embed.add_field(name=f"{language.userinfo_activity_none_title}", value=f'{language.userinfo_activity_none_value}', inline=True)
            else:
                if activity.type == discord.ActivityType.listening:
                    embed.add_field(name=f"{language.userinfo_activity_listening}", value=f'{message.mentions[0].activity.name}', inline=True)

                if activity.type == discord.ActivityType.playing:
                    embed.add_field(name=f"{language.userinfo_activity_playing}", value=f'{message.mentions[0].activity.name}', inline=True)

                if activity.type == discord.ActivityType.streaming:
                    embed.add_field(name=f"{language.userinfo_activity_streaming}", value=f'{message.mentions[0].activity.name}', inline=True)

                if activity.type == discord.ActivityType.watching:
                    embed.add_field(name=f"{language.userinfo_activity_watching}", value=f'{message.mentions[0].activity.name}', inline=True)

            embed.set_thumbnail(url=message.mentions[0].avatar_url)
            setFooter(message, embed)
            await message.channel.send(embed=embed)

            await logger(message)

        except:

            embed = discord.Embed(title=f'{message.author.name}#{message.author.discriminator} {language.userinfo_title}', color=0x15A1EE, timestamp=datetime.datetime.utcnow())

            embed.add_field(name=f"{language.userinfo_username}", value=f'{message.author.name}', inline=True)

            embed.add_field(name=f"{language.userinfo_id}", value=f'{message.author.id}', inline=True)
            created_at = message.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')

            embed.add_field(name=f"{language.userinfo_creation_date}", value=f'{created_at}', inline=True)
            join_date = message.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')

            embed.add_field(name=f"{language.userinfo_join_date}", value=f'{join_date}', inline=True)
            activity = message.author.activity

            if activity is None:
                embed.add_field(name=f"{language.userinfo_activity_none_title}", value=f"{language.userinfo_activity_none_value}", inline=True)
            else:
                if activity.type == discord.ActivityType.listening:
                    embed.add_field(name=f"{language.userinfo_activity_listening}", value=f'{message.author.activity.name}', inline=True)

                if activity.type == discord.ActivityType.playing:
                    embed.add_field(name=f"{language.userinfo_activity_playing}", value=f'{message.author.activity.name}', inline=True)

                if activity.type == discord.ActivityType.streaming:
                    embed.add_field(name=f"{language.userinfo_activity_streaming}", value=f'{message.author.activity.name}', inline=True)

                if activity.type == discord.ActivityType.watching:
                    embed.add_field(name=f"{language.userinfo_activity_watching}", value=f'{message.author.activity.name}', inline=True)


            embed.set_thumbnail(url=message.author.avatar_url)
            setFooter(message, embed)
            await message.channel.send(embed=embed)
            await logger(message)

    #--------------------------#
    #                          #
    #     Stop Command         #
    #                          #
    #--------------------------#


    if message.content.startswith(server_prefix + 'stop'):
       if message.author.id is 220959178779262986 or 200471353516621824:

           embed = discord.Embed(color=0x15A1EE,timestamp=datetime.datetime.utcnow())
           embed.add_field(name=f"{language.stop_title}", value=f"{language.stop_message}", inline=True)
           embed.set_thumbnail(url=client.user.avatar_url)
           await message.channel.send(embed=embed)
           setFooter(message, embed)

           await logger(message)
           await client.logout()

       else:
           await logger(message)

    #--------------------------#
    #                          #
    #    New Ticket Command    #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'new'):

        name = "ticket-" + str(uuid.uuid4()).split("-")[0]

        category = guild.get_channel(server_ticket_category)

        role = discord.utils.get(message.guild.roles, name='Support Team')

        overwrites = {
            message.author: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                mention_everyone=False,
                add_reactions=True),
            role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                mention_everyone=False,
                add_reactions=True),
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            )
        }

        channel = await guild.create_text_channel(name=name, category=category, overwrites=overwrites)

        response_embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
        response_embed.set_author(name=f'Ticket Created', icon_url=message.author.avatar_url)
        response_embed.description = f'Created your ticket at {channel.mention}.'

        await message.channel.send(embed=response_embed)

        ticket = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
        ticket.set_author(name=f'{language.ticket_message_title}', icon_url=message.author.avatar_url)
        ticket.description = f'{language.ticket_message_field1_message}'

        await channel.send(embed=ticket)
        await logger(message)

    #--------------------------#
    #                          #
    #   Close Ticket Command   #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'close'):
        if "ticket" in message.channel.name:

            deletion = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
            deletion.set_author(name=f'{language.ticket_close_author}', icon_url=message.author.avatar_url)
            deletion.description = f'{language.ticket_close_message}'

            await message.channel.send(embed=deletion)

            await asyncio.sleep(5)

            await message.channel.delete()

            await logger(message)

    #--------------------------#
    #                          #
    #      Kick Command        #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'kick'):

        if discord.abc.GuildChannel.permissions_for(message.channel, member=message.author).kick_members:

            try:

                arg = message.content.split()[1]

                await guild.kick(message.mentions[0])

                embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=f"Member Kicked!", value=f"You kicked {message.mentions[0].name} `({message.mentions[0].id})`!", inline=True)
                embed.set_thumbnail(url=message.mentions[0].avatar_url)
                setFooter(message, embed)
                await message.channel.send(embed=embed)

            except:

                embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=f"Error!", value=f"Please enter a member to kick!", inline=True)
                embed.set_thumbnail(url=message.author.avatar_url)
                setFooter(message, embed)
                await message.channel.send(embed=embed)
        else:

            embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
            embed.add_field(name=f"Error!", value=f"You do not have enough perms!", inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            setFooter(message, embed)
            await message.channel.send(embed=embed)


        await logger(message)

    #--------------------------#
    #                          #
    #      Ban Command         #
    #                          #
    #--------------------------#

    if message.content.startswith(server_prefix + 'ban'):

        if discord.abc.GuildChannel.permissions_for(message.channel, member=message.author).ban_members:

            try:

                arg = message.content.split()[1]

                await guild.ban(message.mentions[0])

                embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=f"Member Banned!", value=f"You banned {message.mentions[0].name} `({message.mentions[0].id})`!", inline=True)
                embed.set_thumbnail(url=message.mentions[0].avatar_url)
                setFooter(message, embed)
                await message.channel.send(embed=embed)

            except:

                embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=f"Error!", value=f"Please enter a member to ban!", inline=True)
                embed.set_thumbnail(url=message.author.avatar_url)
                setFooter(message, embed)
                await message.channel.send(embed=embed)
        else:

            embed = discord.Embed(color=0x15A1EE, timestamp=datetime.datetime.utcnow())
            embed.add_field(name=f"Error!", value=f"You do not have enough perms!", inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            setFooter(message, embed)
            await message.channel.send(embed=embed)


        await logger(message)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name=f"{config.website}", type=discord.ActivityType.watching))
    print(f'{language.onready_console}')
    print(f'{client.user.name}#{client.user.discriminator} '
          f'({client.user.id}) {language.onready_start} |'
          f' Created by Chaottiic#0001 (https://chaottiic.com)')


@client.event
async def on_guild_join(guild):

    guild_id = str(guild.id)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    server_file = Path(f"{BASE_DIR}\Discord_Bot\servers\{guild_id}.json")

    if server_file.is_file():

        return

    else:

        shutil.copy('servers/default.json', 'servers/' + str(guild.id) + '.json')
        shutil.copy('servers/ticket/default.json', 'servers/tickets/' + str(guild.id) + '.json')
        print(f'{guild.id} has been created in Bot Data.')


client.run(config.token)
