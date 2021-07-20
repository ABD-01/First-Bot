import discord
import asyncio
import random
import py2048
import blender

TOKEN="ODY1OTY1MTA5NjUzNzk4OTYz.YPLq2g.E9QuNi0DCfsGLjsGZedXxzw3CG4"
GUILD="IvLabs - 2022-2024"

# client = discord.Client()

class CustomClient(discord.Client):
# @client.event
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="cathy help"))
        self.server_chats = dict()
        for server in self.guilds:
            self.server_chats[server.name] = blender.ChatHandler()
        print('The Bot is Ready')


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


        if message.content.lower().startswith('cathy help 2048'):
            await message.reply('Usage: `cathy 2048` or `cathy 2048 <win_condition>`, where win_condition is the highest no. to make.[default: 2048]')

        elif message.content.lower().startswith('cathy help'):
            channel = message.channel
            hembed = discord.Embed(title='Hi, This is Cathy Blender')
            hembed.description = "I'm a bot made by <@701479951479865384> for learning purpose.\nMy prefix is `cathy`"
            hembed.set_thumbnail(url=self.user.avatar_url)
            hembed.add_field(name='Commands', value='`help`, `2048`')
            hembed.add_field(name='Blender AI', value='Use `cathy <your msg>` to chat with me.')
            await message.reply(embed=hembed)


        elif message.content.lower().startswith('cathy 2048'):
            channel = message.channel
            m = message.content.split()
            win_cond = 2048
            if len(m) > 3:
                await message.reply('Usage: `cathy 2048` or `cathy 2048 <win_condition>`')
            elif len(m) == 3:
                try:
                    win_cond = int(m[2])
                    if win_cond > 131072:
                        await message.reply("Wow! That's a huge number. But for your information:"
                                           "\nThe maximum possible value on 4x4 board is `131072`")
                    elif win_cond < 4:
                        await message.reply("Too small `win_condition`. Try again with larger value.")
                    else:
                        await py2048.play_game(self, message, win_cond)
                except ValueError:
                    await message.reply(f"`{m[2]}` is not an integer")
            elif m[1] == '2048':
                await py2048.play_game(self, message, win_cond)


        elif message.content.lower() == 'cathy persona':
            await message.reply(self.server_chats[message.guild.name].personality)

        elif message.content.lower() == 'cathy forget':
            self.server_chats[message.guild.name].say('[DONE]')
            await message.reply('Chat history forgotten.')

        elif message.content.lower().startswith('cathy '):
            saying = message.content[6:]
            self.server_chats[message.guild.name].say(saying)
            response = self.server_chats[message.guild.name].listen()
            await message.reply(response)



client = CustomClient()
client.run(TOKEN)
