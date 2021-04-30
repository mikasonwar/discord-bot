import os

preset_folder = "presets/"

class GuildPreset:
  def __init__(self, name, image):
    self.name = name
    self.image = image

def getGuildPreset(preset_name):
    if not os.path.exists(f"{preset_folder}{preset_name}.txt"):
        return None
    
    name = None
    image = None
    with open(f"{preset_folder}{preset_name}.txt", 'r') as f:
        name = f.read()
    with open(f"{preset_folder}{preset_name}.png", 'rb') as f:
        image = f.read()

    return GuildPreset(name,image)
