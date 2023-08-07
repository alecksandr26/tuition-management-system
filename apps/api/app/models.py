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

class PlanOfPayment(db.Model):
    __tablename__ = "PlanOfPayment"
    
    name = db.Column(db.String(255), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False)
    desc = db.Column(db.Text, nullable = True)
    number_of_classes = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    method = db.Column(db.Integer, nullable = False)

    def __init__(self, name : str, user_id : int, number_of_classes : int,
                 price : float, method : int, desc : str = None):
        assert isinstance(name, str)
        assert isinstance(user_id, int)
        assert isinstance(number_of_classes, int)
        assert isinstance(price, float)
        assert isinstance(method, int)
        if desc != None:
            assert isinstance(desc, str)
            self.desc = desc
            
        self.name = name
        self.user_id = user_id
        self.number_of_classes = number_of_classes
        self.price = price
        self.method = method
        
    def __repr__(self):
        return "<PlanOfPayment {} - {}/{}>".format(self.id, self.user_id, self.name)

class Student(db.Model):
    __tablename__ = "Student"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    plan_name = db.Column(db.String(255), db.ForeignKey("PlanOfPayment.name"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False)
    name = db.Column(db.String(255), nullable = False)
    phone = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = True, unique = True)
    birthday = db.Column(db.Date, nullable = True)
    regdate = db.Column(db.Date, nullable = False)

    def __init__(self, plan_name : str, user_id : int, name : str,
                 phone : str, regdate : datetime.date, email : str = None,
                 birthday : datetime.date = None):
        assert isinstance(plan_name, str)
        assert isinstance(user_id, int)
        assert isinstance(name, str)
        assert isinstance(phone, str)
        assert isinstance(regdate, datetime.date)
        if email != None:
            assert isinstance(email, str)
            self.email = email
        if birthday != None:
            assert isinstance(birthday, datetime.date)
            self.birthday = birthday

        self.plan_name = plan_name
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.regdate = regdate
        
    def __repr__(self):
        return "<Student {} - {}>".format(self.id, self.name)
    

class User(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    name = db.Column(db.String(255), nullable = False)
    passwd = db.Column(db.String(255), nullable = False)
    schoolname = db.Column(db.String(255), nullable = False)

    black_list_token = relationship(BlackListToken, backref = "User", cascade = "all, delete")
    plan_of_payment = relationship(PlanOfPayment, backref = "User", cascade = "all, delete")
    student = relationship(Student, backref = "User", cascade = "all, delete")

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






