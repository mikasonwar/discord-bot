from os import listdir
from os.path import isfile, join
import random

def getFilesFromPath(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def getRandomFileFromPath(path):
    path = f"images/{path}/"
    files = getFilesFromPath(path)
    return f"{path}{random.choice(files)}" 