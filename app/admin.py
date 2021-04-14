from constants import database

def get_admins():
	return database["admins"].fetch_column("user_id")

def is_admin(user_id):
	admins = get_admins()
	return user_id in admins

#Return True for successful, False for admin not found.
def remove_admin(user_id):
	if is_admin(user_id):
		database["admins"].delete(f"user_id = '{user_id}'")
	return False

#Return True for successful, False for already admin.
def add_admin(user_id):
	if is_admin(user_id):
		return False
	database["admins"].insert([user_id])
	return True