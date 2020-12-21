import time
import os
from datetime import date,datetime

class Logger:
    def __init__(self,folder):
        self.folder = folder
        if not os.path.exists(folder):
            os.mkdir(folder)
    
    def writeToFile(self, log_type, file, message):
        file_path = f"{self.folder}/{file}"
        now = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        message = f"[{log_type}]({now}) - {message}\n"
        print(message)

        if os.path.exists(file_path):
            # my eyes hurt
            today = date.today().strftime("%d-%m-%Y")
            created = datetime.strptime(time.ctime(os.path.getctime(file_path)), "%c").strftime("%d-%m-%Y")
            if today != created:
                os.rename(file_path, f"{file_path}.{created}")

        f = open(file_path, "a")
        f.write(message)
        f.close()

    def info(self,message):
        self.writeToFile("INFO", "general.log", message)

    def error(self,message):
        self.writeToFile("ERROR", "general.log", message)

    def warning(self,message):
        self.writeToFile("WARN", "general.log", message)

