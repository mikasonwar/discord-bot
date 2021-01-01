import discord
import random

class RandomPresence:
  def __init__(self, activity, status = discord.Status.online, afk = False):
    self.activity = activity
    self.status = status
    self.afk = afk

PRESENCES = [
    #RandomPresence(activity=discord.Streaming(name="Ver Chads", url="https://discord.io/mikas")), # Testes de Streaming
    #RandomPresence(activity=discord.CustomActivity(name="A ser refém de um orangotango")), # Testes de custom activity
    RandomPresence(activity=discord.Game(name="Tenis numa mesa de pingue-pongo")),
    RandomPresence(activity=discord.Game(name="O Ovo não é uma bola")),
    RandomPresence(activity=discord.Game(name="Habbo")),
    RandomPresence(activity=discord.Game(name="IMVU")),
    RandomPresence(activity=discord.Game(name="VRChat")),
    RandomPresence(activity=discord.Game(name="Olho?")),
    RandomPresence(activity=discord.Game(name="Hasan = Chad")),
    RandomPresence(activity=discord.Game(name="Half life 4")),
    RandomPresence(activity=discord.Game(name="Bati num inglês e o meu pai pagou 2: eletric boogaloo")),
    RandomPresence(activity=discord.Game(name="Há uma pintura de camões a piscar o olho")),
    RandomPresence(activity=discord.Game(name="Tenho de gostar senão sou homofóbico né?")),
    RandomPresence(activity=discord.Game(name="(...) ela quis beijar me e eu fugi para a casa de banho")),
    RandomPresence(activity=discord.Game(name="uma gaja quer vir a minha casa mas não deixo porque ela quer trazer o cão")),
    RandomPresence(activity=discord.Game(name="quem tem de tomar essas decisões não és tu, fazes parte do marketing")),
    RandomPresence(activity=discord.Game(name="Eu prefiro dar o cú, se tu preferes dar as costas...")),
    RandomPresence(activity=discord.Game(name="configuras-me o ts?")),
    RandomPresence(activity=discord.Game(name="Para o ano venho de cosplay")),
    RandomPresence(activity=discord.Game(name="É um cigano que eu conheci na rua")),
    RandomPresence(activity=discord.Game(name="Ele tem cadelas, és só mais uma")),
    RandomPresence(activity=discord.Game(name="não sou manteiga mas por ti derreto")),
    RandomPresence(activity=discord.Game(name="singued soup")),
    RandomPresence(activity=discord.Game(name="kika pede o gustavo em namoro por amor de deus")),
    RandomPresence(activity=discord.Game(name="não mostrou o cú não namora comigo")),
]

def getRandomPresence():
    return random.choice(PRESENCES)
    
    
