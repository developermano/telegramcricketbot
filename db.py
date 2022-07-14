from telegram import user
from tinydb import TinyDB, Query


class tiny:
    def set_user(userid, state):
        db = TinyDB('db.json')
        db.upsert({"userid": userid, "state": state}, Query().userid == userid)

    def get_user_state(userid):
        db = TinyDB('db.json')
        return db.get(Query().userid == userid)['state']
