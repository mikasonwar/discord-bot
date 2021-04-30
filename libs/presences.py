import discord
import libs.database as database
import random

DB = database.getDB()

class RandomPresence:
  def __init__(self, activity, status = discord.Status.online, afk = False):
    self.activity = activity
    self.status = status
    self.afk = afk

PRESENCES = [
    #RandomPresence(activity=discord.Streaming(name="Ver Chads", url="https://discord.io/mikas")), # Testes de Streaming
    #RandomPresence(activity=discord.CustomActivity(name="A ser refém de um orangotango")), # Testes de custom activity
    #RandomPresence(activity=discord.Game(name="Tenis numa mesa de pingue-pongo")),
    "Tenis numa mesa de pingue-pongo",
    "O Ovo não é uma bola",
    "Habbo",
    "IMVU",
    "VRChat",
    "Olho?",
    "Hasan = Chad",
    "Half life 4",
    "Bati num inglês e o meu pai pagou 2: eletric boogaloo",
    "Há uma pintura de camões a piscar o olho",
    "Tenho de gostar senão sou homofóbico né?",
    "(...) ela quis beijar me e eu fugi para a casa de banho",
    "uma gaja quer vir a minha casa mas não deixo porque ela quer trazer o cão",
    "quem tem de tomar essas decisões não és tu, fazes parte do marketing",
    "Eu prefiro dar o cú, se tu preferes dar as costas...",
    "configuras-me o ts?",
    "Para o ano venho de cosplay",
    "É um cigano que eu conheci na rua",
    "Ele tem cadelas, és só mais uma",
    "não sou manteiga mas por ti derreto",
    "singued soup",
    "não mostrou o cú não namora comigo",
]

def setDefaultPresences():
    for p in PRESENCES:
        DB.presence.update_or_insert(DB.presence.value == p,
                            value=p)
        DB.commit()

def addPresence(presence):
    DB.presence.insert(value=presence)
    DB.commit()

def deletePresence(presenceID):
    DB(DB.presence.id == presenceID).delete()
    DB.commit()

def getRandomPresence():
    row = DB(DB.presence.value).select(orderby='<random>').first()
    if(row != None):
        return RandomPresence(activity=discord.Game(name=row.value))
    else:
        return random.choice(PRESENCES)
    
    
