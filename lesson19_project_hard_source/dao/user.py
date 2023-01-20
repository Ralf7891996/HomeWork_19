from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")
        self.session.add(user)
        self.session.commit()

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).get(username)

    def delete(self, uid):
        genre = self.get_one(uid)
        self.session.delete(genre)
        self.session.commit()
