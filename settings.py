import os
import libs.logger as logger
from dotenv import load_dotenv
import libs.permissions as Permissions

VERSION = '1.1.0'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('DISCORD_PREFIX', '!')
logger = logger.Logger("logs")
maintainers = os.getenv('MAINTANERS','151004374053814273,123928976589717510').split(',')
bot_user_role = os.getenv('BOT_USER_ROLE',797498453092859914)
bot_admin_role = os.getenv('BOT_ADMIN_ROLE',797498732035309580)
allow_permissions = os.getenv('ALLOW_PERMISSIONS',"False")=="True" # Allow users with the roles to use commands (Maybe changing this to save in the DB)
permissions = Permissions.Permissions(maintainers, bot_admin_role, bot_user_role, allow_permissions)
mikas_guild = int(os.getenv('MIKAS_GUILD', '331530120445689857'))
mikas_entry_leave = int(os.getenv('MIKAS_ENTRY_LEAVE', '449294623060394015'))
mikas_join_role = int(os.getenv('MIKAS_JOIN_ROLE', '620281670922272780'))
production = os.getenv('PRODUCTION',"False")=="True"