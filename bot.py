import discord
import asyncio
import random
from py2048 import *
TOKEN="NzY5NTYwMzI1Mzg0OTYyMDc5.X5Qy5w.Hwv0eN5jwCJUFxt8rgAGm7EEEk0"
GUILD="Second Years-IvLabs"

# client = discord.Client()

class CustomClient(discord.Client):
# @client.event
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

        elif message.content.startswith('$bruh'):
            channel = message.channel
            await channel.send('Ssup Bruh!')

            def check1(m):
                return 'stupid' in m.content.lower() or 'dump' in m.content.lower() and m.channel == channel
            def check2(m):
                return 'intelligent' in m.content.lower() or 'smart' in m.content.lower() and m.channel == channel

            msg = await self.wait_for('message', check=check1)
            await channel.send("No I'm not <@{}>!".format(msg.author.id))

            msg = await self.wait_for('message', check=check2)
            await channel.send("Yes I am <@{}>!".format(msg.author.id))

        elif message.content.startswith('$help'):
            channel = message.channel
            hembed = discord.Embed(title='Hi, This is First Bot')
            hembed.description = "I'm a bot made by ABD for learning purpose.\nMy prefix is `$`"
            hembed.set_thumbnail(url=self.user.avatar_url)
            hembed.add_field(name='Commands', value='`greet`,`bruh`,`2048`,`emojis`,`icon`,`thumb`,`delete`')
            await channel.send(embed=hembed)

        elif message.content.startswith('$sibam'):
            channel = message.channel
            await channel.send('<:sibam:770188260600447016>')
            # await channel.send(f'Thanks for your appreciation, <@{707967110382485566}>')
            await message.delete()

        elif message.content.startswith('$emojis'):
            guild = message.guild
            channel = message.channel
            eembed = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}", footer='Page 1/3')
            eembed2 = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}", footer='Page 2/3')
            eembed3 = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}", footer='Page 3/3')
            # msg = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name} id={emoji.id} \n' for emoji in guild.emojis)
            msg = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name}, {emoji.id}\n' for emoji in guild.emojis[:15])
            msg2 = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name}, {emoji.id}\n' for emoji in guild.emojis[18:33])
            msg3 = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name}, {emoji.id}\n' for emoji in guild.emojis[33:])
            eembed.add_field(name='Emojis', value=msg)
            eembed2.add_field(name='Emojis', value=msg2)
            eembed3.add_field(name='Emojis', value=msg3)
            print(len(msg))
            print(len(msg2))
            print(len(msg3))
            embedmsg = await channel.send(embed=eembed)
            await channel.send(embed=eembed2)
            await channel.send(embed=eembed3)

        elif message.content.startswith('$icon'):
            guild = message.guild
            channel = message.channel
            await channel.send(guild.icon_url)

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
                    reaction, user = await client.wait_for('reaction_add', timeout=1, check=checkdown)
                    print(bm.reactions)
                except asyncio.TimeoutError:
                    pass
                else:
                    await channel.send('Noice')
                    break

                await bm.edit(content='Send me that 👍 reaction, <@{}>!'.format(message.author.id))
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=1, check=checkup)
                    print(bm.reactions)
                except asyncio.TimeoutError:
                    pass
                else:
                    await channel.send('Noice')
                    break

        elif message.content.startswith('$2048'):
            channel = message.channel
            author = message.author
            m = message.content.split('$2048')
            win_cond = 2048
            if len(m) > 1 and '-w' in message.content:
                try:
                    win_cond = int(m[1].split('-w')[1])
                    if win_cond>4096:
                        win_cond = 4096
                except ValueError:
                    await channel.send(f"{m[1].split('-w')[1]} is not an integer", delete_after=3)

            emojis = ['⬅️', '⬆️', '⬇️', '➡️', '❌']

            win_cond, game_board = start_game(win_cond=win_cond, board_size=4)
            # desc = f"Use the letters `w`,`a`,`s`,`d` to Play.\n Use `q` or `Quit` to stop the game\nYour `win_conditon` is `{win_cond}`"
            desc = f"""Use {emojis[0]},{emojis[1]},{emojis[2]},{emojis[3]} to Play.\n 
                    Use {emojis[4]} to stop the game\nYour `win_conditon` is `{win_cond}`"""

            color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
            color = int(color, 16)
            embed = discord.Embed(title='2048', description=desc, color=color)
            embed.set_footer(text=f'{author.name}', icon_url=author.avatar_url)
            # embed.add_field(name='Usage', value='`$2048 -w <win_cond>`', inline=False)

            strboard = printboard(game_board)
            embed.add_field(name='Board', value=strboard)
            bemsg = await channel.send(embed=embed)

            def check(reaction, user):
                # return m.author == message.author and m.channel == channel
                emojis = ['⬅️', '⬆️', '⬇️', '➡️', '❌']
                return user == author and str(reaction.emoji) in emojis

            async def addallemoj(bemsg,emojis):
                for emoji in emojis:
                    await bemsg.add_reaction(emoji)

            def emojitochar(reaction):
                emoj = str(reaction.emoji)
                if emoj == emojis[0]:
                    return 'a'
                elif emoj == emojis[1]:
                    return 'w'
                elif emoj == emojis[2]:
                    return 's'
                elif emoj == emojis[3]:
                    return 'd'
                else:
                    return 'q'

            await addallemoj(bemsg, emojis)

            while True:
                # await addallemoj(bemsg, emojis)
                try:
                    # msg = await self.wait_for('message',timeout=60, check=check)
                    reaction, user = await client.wait_for('reaction_add', timeout=60, check=check)
                    await bemsg.remove_reaction(reaction, user)
                    print('Received reaction', reaction, 'from', user)
                except asyncio.TimeoutError:
                    # await channel.send(f'<@{author.id}> did not respond in time, what a noob!')
                    embed.add_field(name='Result', value=f'<@{author.id}>, did not respond in time, SED', inline=False)
                    await bemsg.edit(embed=embed)
                    break
                else:
                    ch = emojitochar(reaction)
                    # ch = msg.content
                    # checking if entered key is correct
                    if ch.lower() in ['a', 's', 'd', 'w']:
                        if isValid(ch, game_board) == False:
                            print("Invalid move = ", ch)
                            # await channel.send(f'<@{author.id}> That\'s an invalid move', delete_after=2)
                            embed.add_field(name='Invalid Move', value=f'{reaction.emoji} is Invalid Move', inline=False)
                            await bemsg.edit(embed=embed)
                            embed.remove_field(1)
                            continue
                        else:
                            ##print("You pressed", ch)
                            game_board = game_move(ch, game_board)
                            game_board = insert_two(game_board)
                            strboard = printboard(game_board)
                            # embed.clear_fields()
                            # embed.add_field(name='Board', value=strboard)
                            embed.set_field_at(index=0, name='Board', value=strboard)
                            await bemsg.edit(embed=embed)
                            # await msg.delete(delay=0.5)

                            # Checking the game progress
                            if didLose(game_board) == True:
                                print('Game Over, You Lose')
                                # await channel.send(f'<@{author.id}> You Lose')
                                embed.add_field(name='Result', value=f'<@{author.id}>, You Lost ☹️', inline=False)
                                await bemsg.edit(embed=embed)
                                break

                            # checking for winning Criteria
                            if didWin(win_cond,game_board) == True:
                                print('You Win')
                                # await channel.send(f'<@{author.id}> You Won')
                                embed.add_field(name='Result', value=f'<@{author.id}>, You Won 🏆', inline=False)
                                await bemsg.edit(embed=embed)
                                break

                    # If user wants to quit b/w gthe game
                    elif ch.lower() in ['q', 'quit']:
                        # await channel.send(f'<@{author.id}> , Oh no! You Gave Up, SED!')
                        embed.add_field(name='Result', value=f'<@{author.id}>, You Gave Up 😞', inline=False)
                        await bemsg.edit(embed=embed)
                        break

                    # In anyother case Re-propmt
                    # else:
                    #     print("Invalid Key = ", ch)
                    #     await channel.send(f'<@{author.id}> That\'s an invalid key', delete_after=2)
                    #     await msg.delete(delay=0.5)
                    #     continue




        elif message.content.startswith('$user'):
            channel = message.channel
            author = message.author
            print(author)
            dmsg = await author.send('hello')
            print(dmsg)
            print(dmsg.channel)
            print(dmsg.channel.type)
            print(dmsg.channel == 'dm')

        elif message.content.startswith('$send'):
            channel = message.channel
            author = message.author
            print(author,channel)

        elif message.content.startswith('$msg'):
            channel = message.channel
            msg = await channel.fetch_message('770068405814296597')
            print(msg.author)
            #dmsg = await msg.author.send('Hi Bro!!')
            dmchannel = msg.author.dm_channel
            messages = await dmchannel.history(limit=123).flatten()
            print(messages)

        elif message.content.startswith('$react'):
            emojis = ['⬅️', '⬆️', '⬇️', '➡️', '❌']
            for emoji in emojis:
                await message.add_reaction(emoji)
            while True:
                reaction, user = await client.wait_for('reaction_add', timeout=60, check=lambda reaction,user : user ==message.author)
                await message.remove_reaction(reaction, user)

        elif message.content.startswith('$embed'):
            color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
            color = int(color, 16)
            embed = discord.Embed(title='Tile', color=color, url='https://www.github.com/ABD-01', description='Description')
            embed.set_footer(text='Footer', icon_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F2674081007769600%2F&psig=AOvVaw0wUZmMZ9D5KzERMhjo1-ZA&ust=1605433821629000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCPjX-5rhge0CFQAAAAAdAAAAABAD')
            embed.set_image(url=self.user.avatar_url)
            embed.set_thumbnail(url='https://i.pinimg.com/originals/24/30/bb/2430bbe2bea760f0e011a56e5d11f2cf.jpg')
            embed.set_author(name='ABD',url='https://www.linkedin.com/in/abd931/', icon_url='https://images-ext-2.discordapp.net/external/HVCvJmDFnE7C29KNusmLJQDPeA5Pg7kOvKvOdf9YyX8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/701479951479865384/40265d228c5d5e6ba3142e2b3fcc5d6d.webp')
            embed.add_field(name='Field 1', value='Value 1', inline=False)
            embed.add_field(name='Field 2', value='Value 2', inline=True)
            embed.add_field(name='Field 3', value='Value 3', inline=True)
            msg = await message.channel.send('Embede Message', embed=embed)
            await asyncio.sleep(5)
            embed.remove_field(1)
            await msg.edit(content='Edited Embed', embed=embed)



client = CustomClient()
client.run(TOKEN)

