import discord
import asyncio
import random
import py2048

TOKEN="NzY5NTYwMzI1Mzg0OTYyMDc5.X5Qy5w.Hwv0eN5jwCJUFxt8rgAGm7EEEk0"
GUILD="Second Years-IvLabs"

# client = discord.Client()

class CustomClient(discord.Client):
    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == GUILD:
                break

        # print(
        #     f'{self.user} is connected to the following guild:\n'
        #     f'{guild.name}(id: {guild.id})\n'
        # )

        print('The Bot is Ready')

        # print('server emojis')
        # print(guild.emojis)


    # @client.event
    async def on_message(self,message):
        if message.content.startswith('$greet'):
            channel = message.channel
            await channel.send('Say hello!')

            def check(m):
                return m.content.lower() == 'hello' and m.channel == channel

            msg = await self.wait_for('message', check=check)
            # '<@&%s>' % self.id
            await channel.send('Hello <@%s>!' % msg.author.id)


        elif message.content.startswith('$help'):
            channel = message.channel
            hembed = discord.Embed(title='Hi, This is First Bot')
            hembed.description = "I'm a bot made by ABD for learning purpose.\nMy prefix is `$`"
            hembed.set_thumbnail(url=self.user.avatar_url)
            hembed.add_field(name='Commands', value='`greet`,`2048`,`emojis`,`icon`,`thumb`,`delete`')
            await channel.send(embed=hembed)


        elif message.content.startswith('$clear'):
            channel = message.channel
            m = message.content.split()
            if len(m) != 2:
                await channel.send('Usage: `$clear no_of_messages`')


        elif message.content.startswith('$delete'):
            channel = message.channel
            msg = message.content.split('$delete')
            if message.content.strip() == '$delete':
                await channel.send('Usage: `$delete <msg_id>,<msg_id>, ..`', delete_after=3)
            else:
                ids = msg[1].split(',')
                for id in ids:
                    try:
                        delmesg = await channel.fetch_message(id.strip())
                        await delmesg.delete(delay=0.5)
                        await channel.send('I deleted the message', delete_after=1)
                        print('Deleted', delmesg.content)
                    except Exception as e:
                        await channel.send('Error: '+str(e), delete_after=2)
                        print(e)
                        print(id)
            print(message)
            await message.delete(delay=0.5)


        elif message.content.startswith('$thumb'):
            channel = message.channel
            bm = await channel.send('Send me that 👍 reaction, <@{}>!'.format(message.author.id))

            await bm.add_reaction('👍')
            await bm.add_reaction('👎')

            def checkup(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍'
            def checkdown(reaction, user):
                return user == message.author and str(reaction.emoji) == '👎'
            while True:
                await bm.edit(content='Send me that 👎 reaction, <@{}>!'.format(message.author.id))
                try:
                    reaction, user = await self.wait_for('reaction_add', timeout=1, check=checkdown)
                    await bm.remove_reaction(reaction, user)
                    print(bm.reactions)
                except asyncio.TimeoutError:
                    pass
                else:
                    await channel.send('Noice')
                    break

                await bm.edit(content='Send me that 👍 reaction, <@{}>!'.format(message.author.id))
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=1, check=checkup)
                    await bm.remove_reaction(reaction, user)
                    print(bm.reactions)
                except asyncio.TimeoutError:
                    pass
                else:
                    await channel.send('Noice')
                    break

        elif message.content.startswith('$2048'):
            channel = message.channel
            m = message.content.split()
            win_cond = 2048
            if len(m) > 2:
                await channel.send('Usage: `$2048` or `$2048 win_condition`')
            elif len(m) == 2:
                try:
                    win_cond = int(m[1])
                    if win_cond > 131072:
                        await channel.send("Wow! That's a huge number. But for your information:"
                                           "\nThe maximum possible value on 4x4 board is `131072`")
                    else:
                        await py2048.play_game(self, message, win_cond)
                except ValueError:
                    await channel.send(f"`{m[1]}` is not an integer")
            elif m[0] == '$2048':
                await py2048.play_game(self, message, win_cond)


        # elif message.content.startswith('$msguser'):
        #     userids = {'abd':701479951479865384, 'kira':761989402725187635 , 'luqman':707968621238026310 , 'sibam':393298417704501248}
        #     hembed = discord.Embed(title='Hi, This is First Bot')
        #     hembed.description = "I'm a bot made by ABD for learning purpose.\nMy prefix is `$`"
        #     hembed.set_thumbnail(url=self.user.avatar_url)
        #     hembed.add_field(name='Commands', value='`greet`,`bruh`,`2048`,`emojis`,`icon`,`thumb`,`delete`')
        #     a = await self.fetch_user(userids['abd'])
        #     print(a)
        #     await message.author.send(a)
        #     msg = await a.send(embed=hembed)
        #     print(msg)
        #     await a.send('Try `$2048` command now. It\'s usage is `$2048 -w win_cond`')
        #     messages = await msg.channel.history(limit=123).flatten()
        #     for me in messages:
        #         print(me.author, me.content)
        #         '''await message.author.send(content=(f'`{me.author}`', me.content))
        #         if me.embeds:
        #             for e in me.embeds:
        #                 print(me.author, e.to_dict())
        #                 await message.author.send(content=f'`{me.author}`:', embed=e)'''
        #         if me.author == self.user:
        #             await me.delete()


        elif message.content.startswith('$permission'):
            author = message.author
            print(author.guild_permissions)
            m =  await message.channel.send('Looking for permissions...')
            #p = author.guild_permissions
            p = m.author.guild_permissions
            print(p.general())
            print(p.text())
            print(p.voice())
            print(p.create_instant_invite)
            print(p.kick_members)
            print(p.ban_members)
            print(p.administrator)
            print(p.manage_channels)
            print(p.manage_guild)
            print(p.manage_messages)





client = CustomClient()
client.run(TOKEN)
