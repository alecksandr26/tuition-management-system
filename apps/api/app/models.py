from app.extensions import db
from sqlalchemy.orm import relationship
import datetime


class BlackListToken(db.Model):
    __tablename__ = "BlackListtoken"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    token = db.Column(db.String(500), unique = True, nullable = False)
    blacklisted_on = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False)

    def __init__(self, token : str, user_id : int):
        assert isinstance(token, str)
        assert isinstance(user_id, int)
        
        self.token = token
        self.user_id = user_id
        self.blacklisted_on = datetime.datetime.now()
        
    def __repr__(self):
        return "<BlackListToken {} - {}>".format(self.id, self.user_id)

class User(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    name = db.Column(db.String(255), nullable = False)
    passwd = db.Column(db.String(255), nullable = False)
    schoolname = db.Column(db.String(255), nullable = False)

    black_list_token = relationship(BlackListToken, backref = 'User', passive_deletes = "all")

    def __init__(self, name : str, email : str, passwd : str, schoolname : str):
        assert isinstance(name, str)
        assert isinstance(email, str)
        assert isinstance(passwd, str)
        assert isinstance(schoolname, str)

        self.name = name
        self.email = email
        self.passwd = passwd
        self.schoolname = schoolname

    def __repr__(self):
        return "<User {} - {}>".format(self.id, self.name)

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "email" : self.email,
            "schoolname" : self.schoolname
        }


