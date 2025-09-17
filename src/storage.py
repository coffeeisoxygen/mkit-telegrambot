from tinydb import Query, TinyDB


class UserStorage:
    def __init__(self, db_path="users.json"):
        self.db = TinyDB(db_path)
        self.UserQ = Query()

    def is_user_approved(self, uid):
        res = self.db.search(self.UserQ.user_id == uid)
        return bool(res and res[0]["status"] == "approved")

    def add_pending_user(self, uid, name):
        if not self.db.search(self.UserQ.user_id == uid):
            self.db.insert({"user_id": uid, "name": name, "status": "pending"})

    def update_user_status(self, uid, status):
        self.db.update({"status": status}, self.UserQ.user_id == uid)

    def get_pending_users(self):
        return self.db.search(self.UserQ.status == "pending")
