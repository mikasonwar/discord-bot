import libs.database as database

DB = database.getDB()

def remember_user_roles(user_id, roles):
    if get_user_roles(user_id) is not None:
        delete_user_roles(user_id)
        

    DB.user_roles.insert(user_id=user_id, roles=roles)
    DB.commit()

def delete_user_roles(user_id):
    DB(DB.user_roles.user_id == user_id).delete()
    DB.commit()

def delete_all_user_roles():
    DB(DB.user_roles).delete()
    DB.commit()

def get_user_roles(user_id):
    result = DB(DB.user_roles.user_id == user_id).select(DB.user_roles.roles).first()
    if result is None:
        return None
    else:
        return result.roles.split(";")