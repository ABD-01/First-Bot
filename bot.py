import discord
TOKEN="NzY5NTYwMzI1Mzg0OTYyMDc5.X5Qy5w.Hwv0eN5jwCJUFxt8rgAGm7EEEk0"
GUILD="Second Years-IvLabs"

client = discord.Client()

class CustomClient(discord.Client):
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

        print('server members')
        print(len(guild.members))

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
            hembed = discord.Embed(title='Hi')
            hembed.description = "I'm a bot made by ABD for learning purpose.\nMy prefix is `$`"
            hembed.set_thumbnail(url=self.user.avatar_url)
            hembed.add_field(name='Commands', value='`greet`,`bruh`,`sibam`,`emojis`,`icon`,`thumb`')
            await channel.send(embed=hembed)

        elif message.content.startswith('$sibam'):
            channel = message.channel
            await channel.send('<:sibam:760903346051350537>')

        elif message.content.startswith('$emojis'):
            for guild in self.guilds:
                if guild.name == GUILD:
                    break
            channel = message.channel
            eembed = discord.Embed(title='Server Emojis', description=f"Following are the emojis of {guild.name}")
            eembed2 = discord.Embed()
            eembed3 = discord.Embed()
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
            await channel.send(embed=eembed)
            await channel.send(embed=eembed2)
            await channel.send(embed=eembed3)

        # elif message.content.startswith('$roles'):
        #     for guild in self.guilds:
        #         if guild.name == GUILD:
        #             break
        #     channel = message.channel
        #     for role in guild.roles:
        #         msg = f'name={role.name}, id={role.id} '
        #         await channel.send(msg)

        elif message.content.startswith('$icon'):
            for guild in self.guilds:
                if guild.name == GUILD:
                    break
            channel = message.channel
            await channel.send(guild.icon_url)

        elif message.content.startswith('$thumb'):
            channel = message.channel
            await channel.send('Send me that 👍 reaction, {.author}'.format(message))

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await channel.send('👍')


client = CustomClient()
client.run(TOKEN)

