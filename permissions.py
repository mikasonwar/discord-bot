from discord.ext import commands

# Futuramente a ver se é implementado com BD
class Permissions:
    def __init__(self, maintainers, admin_role_id, user_role_id, allow_permissions):
        self.maintainers = maintainers
        self.admin_role = admin_role_id
        self.user_role = user_role_id
        self.allow_permissions = allow_permissions

    def setAllowPermissions(self, allow_permissions):
        self.allow_permissions = allow_permissions

    def isMaintainer(self):
        async def predicate(ctx):
            return str(ctx.message.author.id) in self.maintainers
        return commands.check(predicate) 

    def isAdmin(self):
        permissions = self
        async def predicate(ctx):
            if await permissions.isMaintainer().predicate(ctx):
                return True

            if permissions.allow_permissions == False:
                return False

            return await commands.has_permissions(administrator=True).predicate(ctx) or await commands.has_role(permissions.admin_role).predicate(ctx)
        return commands.check(predicate) 