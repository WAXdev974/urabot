#_______________.___.  __      __  _____  ____  ___
#\______   \__  |   | /  \    /  \/  _  \ \   \/  /
# |    |  _//   |   | \   \/\/   /  /_\  \ \     / 
# |    |   \\____   |  \        /    |    \/     \ 
# |______  // ______|   \__/\  /\____|__  /___/\  \
#        \/ \/               \/         \/      \_/



import discord
from discord import app_commands

from discord.ext import commands, tasks
import random
import asyncio

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = "+", intents = intents)
bot.remove_command("help")
status = ["Prefix +",
          "Version : 1.0"]
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

intents = discord.Intents.default()
intents.typing = False
intents.presences = False


sondages = {}
tickets = []

@bot.event
async def on_ready():
    print(f"{bot.user.name} bot open")
    changeStatus.start()


@bot.event
async def on_member_join(member):
    
    welcome_message = f'Bienvenue sur **Uranium pvp Faction** '

    
    await member.send(welcome_message)
    print(f"Message envoyé à {member.name}")



@bot.command
async def start(ctx, secondes = 10):
    changeStatus.change_interval(sec = secondes)

@tasks.loop(seconds = 10)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status = discord.Status.online, activity = game)

@bot.command()
async def warn(ctx, member: discord.Member, *, reason):
    
    if ctx.message.author.guild_permissions.manage_messages:
        
        try:
            await member.send(f"Vous avez été **averti** par {ctx.message.author.name} pour la raison suivante: {reason}")
        except discord.Forbidden:
            await ctx.send("Je ne peux pas envoyer de messages privés à cet utilisateur.")
        else:
            await ctx.send(f"{member.mention} a été averti pour la raison suivante: {reason}")
    else:
        await ctx.send("Vous n'avez pas la permission de donner un avertissement.")


@bot.command()
async def ip(ctx):
    await ctx.send("*Notre IP*")
    await ctx.send("**uranium-pvp.fr**")
    await ctx.send("**19132**")
    await ctx.message.delete()
    print(f"IP drop")

@bot.command()
async def site(ctx):
    await ctx.send("notre site : https://uranium-pvp.fr")
    await ctx.message.delete()
    print(f"link website drop")

@bot.command()
async def clear(ctx, amount=5):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)  
        await ctx.send(f'{amount} messages ont été **supprimés** par {ctx.author.mention}', delete_after=5)  
    else:
        await ctx.send("Vous n'avez pas la permission de gérer les messages.")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.ban_members:
        
        await member.ban(reason=reason)
        
        
        await ctx.send(f'{member.mention} a été **banni**. Raison : {reason}')
        
        
        if reason is not None:
            dm_message = f"Vous avez été banni par {ctx.author.display_name} pour la raison suivante : {reason}"
        else:
            dm_message = f"Vous avez été banni par {ctx.author.display_name} sans raison spécifiée."
        
        try:
            await member.send(dm_message)
        except discord.Forbidden:
            
            await ctx.send("Impossible d'envoyer un message en DM au membre banni (DM désactivés).")
    else:
        await ctx.send("Vous n'avez pas la permission de bannir des membres.")



@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.kick_members:
        if member.guild_permissions.administrator:
            await ctx.send("Vous ne pouvez pas kicker un administrateur.")
        else:
            await member.kick(reason=reason)
            await ctx.send(f'{member.mention} a été **kick**.')
    else:
        await ctx.send("Vous n'avez pas la permission de kick des membres.")


@bot.command()
async def unban(ctx, *, member_id):
    await ctx.message.delete()
    if ctx.author.guild_permissions.ban_members:
        try:
            
            member = await bot.fetch_user(int(member_id))
            
            
            await ctx.guild.unban(member)
            
            
            await ctx.send(f'{member.name}#{member.discriminator} a été **débanni**.')
        except discord.NotFound:
            await ctx.send(f'Aucun utilisateur avec l\'ID {member_id} n\'a été trouvé.')
    else:
        await ctx.send('Vous n\'avez pas la permission de débanir des membres.')



@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if role not in member.roles:
        await member.add_roles(role)
        await ctx.send(f"{role.name} a été ajouté à {member.display_name}")
    else:
        await ctx.send(f"{member.display_name} a déjà le rôle {role.name}")


@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"{role.name} a été retiré de {member.display_name}")
    else:
        await ctx.send(f"{member.display_name} n'a pas le rôle {role.name}")


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: int, *, reason=None):
        guild = ctx.guild
        
        duration = duration * 60  
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} a été **temporairement banni** pour {duration // 60} minutes. Raison : {reason}")
        await asyncio.sleep(duration)
        await guild.unban(member)
        await ctx.send(f"{member.mention} a été **débanni** après {duration // 60} minutes.")

def setup(bot):
    bot.add_cog(Mod(bot))


@bot.command()
async def mute(ctx, member: discord.Member, duration: int):
    
    if ctx.author.guild_permissions.manage_roles:
       
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            await ctx.send("Le rôle 'Muted' n'existe pas. Créez-le avant d'utiliser cette commande.")
            return

       
        await member.add_roles(muted_role)

        
        await asyncio.sleep(duration)
        await member.remove_roles(muted_role)

        await ctx.send(f"{member.mention} a été **temporairement muté** pour {duration} secondes.")
    else:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour utiliser cette commande.")


@bot.command(name='sondage')
async def create_sondage(ctx, *question):
    question = ' '.join(question)
    sondages[ctx.channel.id] = {'question': question, 'votes': {}}
    await ctx.send(f'Sondage créé : {question}')

@bot.command(name='end_sondage')
async def end_sondage(ctx):
    if ctx.channel.id in sondages:
        sondage = sondages[ctx.channel.id]
        question = sondage['question']
        votes = sondage['votes']
        await ctx.send(f'Sondage terminé : {question}')
        await ctx.send('Résultats du sondage :')
        for option, count in votes.items():
            await ctx.send(f'{option}: {count} vote(s)')
        del sondages[ctx.channel.id]
    else:
        await ctx.send('Aucun sondage en cours dans ce salon.')

@bot.command()
async def say(ctx, *, message):
    await  ctx.message.delete()
    await ctx.send(message) 
    print(f"Message bien envoyer {message}")    


@bot.command()
async def ticket(ctx, *, transcript: str):
    
    ticket_info = {
        "transcript": transcript,
        "status": "Open",
        "claimer": None
    }
    
  
    tickets.append(ticket_info)
    
   
    await ctx.send(f"Ticket créé avec le transcript : {transcript}")


@bot.command()
async def close(ctx, ticket_id: int):
 
    if 0 <= ticket_id < len(tickets):
        tickets[ticket_id]["status"] = "Closed"
        await ctx.send(f"Ticket {ticket_id} a été fermé.")
    else:
        await ctx.send("Ticket introuvable.")


@bot.command()
async def open(ctx, ticket_id: int):
    
    if 0 <= ticket_id < len(tickets):
        tickets[ticket_id]["status"] = "Open"
        await ctx.send(f"Ticket {ticket_id} a été rouvert.")
    else:
        await ctx.send("Ticket introuvable.")


@bot.command()
async def claim(ctx, ticket_id: int):
   
    if 0 <= ticket_id < len(tickets):
        tickets[ticket_id]["claimer"] = ctx.author
        await ctx.send(f"Ticket {ticket_id} a été revendiqué par {ctx.author.mention}.")
    else:
        await ctx.send("Ticket introuvable.")

@bot.command()
async def accsupport(ctx, *, message):
    await ctx.send(f"Votre ticket a été pris en charge par {message}")
    await ctx.message.delete()
    print(f"ticket {message}")

bot.run("token_bot")