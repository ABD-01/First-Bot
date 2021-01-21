import discord
import asyncio
import py2048


async def firstbot(bot, message):

    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content.lower() == 'hello' and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        # '<@&%s>' % self.id
        await channel.send('Hello <@%s>!' % msg.author.id)


    elif message.content.startswith('$help 2048'):
        await message.channel.send('Usage: `$2048` or `$2048 win_condition`')

    elif message.content.startswith('$help'):
        channel = message.channel
        hembed = discord.Embed(title='Hi, This is First Bot')
        hembed.description = "I'm a bot made by ABD for learning purpose.\nMy prefix is `$`"
        hembed.set_thumbnail(url=bot.user.avatar_url)
        hembed.add_field(name='Commands', value='`greet`,`2048`,`thumb`,`delete`')
        chat_channel = discord.utils.get(message.guild.text_channels, name="chat-aiml")
        if chat_channel is None:
            hembed.add_field(name='AIML Chat', value='''Have a talk with we in `#chat-aiml` channel.
                                                        (You need to create `#chat-aiml` channel if it doesn't exists.)''', inline=False)
        else:
            hembed.add_field(name='AIML Chat', value=f"Have a talk with we in {chat_channel.mention} channel.", inline=False)
        await channel.send(embed=hembed)


    # elif message.content.startswith('$clear'):
    #     channel = message.channel
    #     m = message.content.split()
    #     if len(m) != 2:
    #         await channel.send('Usage: `$clear no_of_messages`')


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
                    # print('Deleted', delmesg.content)
                except Exception as e:
                    await channel.send('Error: '+str(e), delete_after=2)
                    # print(e)
                    # print(id)
        # print(message)
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
                reaction, user = await bot.wait_for('reaction_add', timeout=1, check=checkdown)
                await bm.remove_reaction(reaction, user)
                print(bm.reactions)
            except asyncio.TimeoutError:
                pass
            else:
                await channel.send('Noice')
                break

            await bm.edit(content='Send me that 👍 reaction, <@{}>!'.format(message.author.id))
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=1, check=checkup)
                await bm.remove_reaction(reaction, user)
                print(bm.reactions)
            except asyncio.TimeoutError:
                pass
            else:
                await channel.send('Noice')
                break

    # elif message.content.startswith('$say'):
    #     channel = message.channel
    #     msg = message.content.split('$say')
    #     if message.content.strip() == '$say':
    #         await channel.send('Usage: `$say -c <channel> -m <message>`', delete_after=3)


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
                    await py2048.play_game(bot, message, win_cond)
            except ValueError:
                await channel.send(f"`{m[1]}` is not an integer")
        elif m[0] == '$2048':
            await py2048.play_game(bot, message, win_cond)

