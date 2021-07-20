import discord
import asyncio
import random
import py2048

TOKEN="ODY1OTY1MTA5NjUzNzk4OTYz.YPLq2g.E9QuNi0DCfsGLjsGZedXxzw3CG4"
GUILD="IvLabs - 2022-2024"

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
        # if message.content.startswith('$greet'):
        #     channel = message.channel
        #     await channel.send('Say hello!')

        #     def check(m):
        #         return m.content.lower() == 'hello' and m.channel == channel

        #     msg = await self.wait_for('message', check=check)
        #     # '<@&%s>' % self.id
        #     await channel.send('Hello <@%s>!' % msg.author.id)


        elif message.content.startswith('cathy help'):
            channel = message.channel
            hembed = discord.Embed(title='Hi, This is Cathy Blender')
            hembed.description = "I'm a bot made by ABD for learning purpose.\nMy prefix is `cathy`"
            hembed.set_thumbnail(url=self.user.avatar_url)
            hembed.add_field(name='Commands', value='`help`, `<msg>`, `2048`')
            await channel.send(embed=hembed)


        elif message.content.startswith('cathy 2048'):
            channel = message.channel
            m = message.content.split()
            win_cond = 2048
            if len(m) > 2:
                await channel.send('Usage: `cathy 2048` or `cathy 2048 <win_condition>`')
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






client = CustomClient()
client.run(TOKEN)
