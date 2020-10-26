import discord
import asyncio
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

        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

        print('server emojis')
        print(guild.emojis)


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
            hembed.add_field(name='Commands', value='`greet`,`bruh`,`2048`,`sibam`,`emojis`,`icon`,`thumb`,`delete`')
            await channel.send(embed=hembed)

        elif message.content.startswith('$sibam'):
            channel = message.channel
            await channel.send('<:sibam:760903346051350537>')

        elif message.content.startswith('$emojis'):
            # for guild in self.guilds:
            #     if guild.name == GUILD:
            #         break
            guild = message.guild
            channel = message.channel
            eembed = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}", footer='Page 1/3')
            eembed2 = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}", footer='Page 2/3')
            eembed3 = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}", footer='Page 3/3')
            # msg = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name} id={emoji.id} \n' for emoji in guild.emojis)
            msg = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name}\n' for emoji in guild.emojis[:15])
            msg2 = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name}\n' for emoji in guild.emojis[15:31])
            msg3 = "".join(f'<:{emoji.name}:{emoji.id}> {emoji.name}\n' for emoji in guild.emojis[31:])
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
            # for guild in self.guilds:
            #     if guild.name == GUILD:
            #         break
            guild = message.guild
            channel = message.channel
            await channel.send(guild.icon_url)

        elif message.content.startswith('$delete'):
            channel = message.channel
            msg = message.content.split('$delete')
            if len(msg) < 2:
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
                except ValueError:
                    await channel.send(f"{m[1].split('-w')[1]} is not an integer", delete_afer=5)

            win_cond, game_board = start_game(win_cond=win_cond, board_size=4)
            desc = f"Use the letters `w`,`a`,`s`,`d` to Play.\n Use `q` or `Quit` to stop the game\nYour `win_conditon` is `{win_cond}`"
            embed = discord.Embed(title='2048', description=desc)
            embed.set_footer(text=f'{author.name}', icon_url=author.avatar_url)

            strboard = printboard(game_board)
            embed.add_field(name='Board', value=strboard)
            bemsg = await channel.send(embed=embed)

            def check(m):
                return m.author == message.author and m.channel == channel

            while True:
                try:
                    msg = await self.wait_for('message',timeout=60, check=check)
                except asyncio.TimeoutError:
                    await channel.send(f'<@{author.id}> did not respond in time, what a noob!')
                    break
                else:
                    ch = msg.content
                    # checking if entered key is correct
                    if ch.lower() in ['a', 's', 'd', 'w']:
                        if isValid(ch, game_board) == False:
                            print("Invalid move = ", ch)
                            await channel.send(f'<@{author.id}> That\'s an invalid move', delete_after=2)
                            await msg.delete(delay=0.5)
                            continue
                        else:
                            ##print("You pressed", ch)
                            game_board = game_move(ch, game_board)
                            game_board = insert_two(game_board)
                            strboard = printboard(game_board)
                            embed.clear_fields()
                            embed.add_field(name='Board', value=strboard)
                            await bemsg.edit(embed=embed)
                            await msg.delete(delay=0.5)

                            # Checking the game progress
                            if didLose(game_board) == True:
                                print('Game Over, You Lose')
                                await channel.send(f'<@{author.id}> You Lose')
                                break

                            # checking for winning Criteria
                            if any(win_cond in row for row in game_board) == True:
                                print('You Win')
                                await channel.send(f'<@{author.id}> You Won')
                                break

                    # If user wants to quit b/w gthe game
                    elif ch.lower() in ['q', 'quit']:
                        await channel.send(f'<@{author.id}> , Oh no! You Gave Up, SED!')
                        break

                    # In anyother case Re-propmt
                    else:
                        print("Invalid Key = ", ch)
                        await channel.send(f'<@{author.id}> That\'s an invalid key', delete_after=2)
                        await msg.delete(delay=0.5)
                        continue


client = CustomClient()
client.run(TOKEN)

