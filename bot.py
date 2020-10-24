import discord
TOKEN="NzY5NTYwMzI1Mzg0OTYyMDc5.X5Qy5w.Hwv0eN5jwCJUFxt8rgAGm7EEEk0"
client = discord.Client()
 
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
