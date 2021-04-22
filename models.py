from datetime import datetime
from werkzeug import generate_password_hash  , check_password_hash
from app import db 

class Admin(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(120) ,index=True)
    phone = db.Column(db.String(10), nullable = True)
    password_hash = db.Column(db.String(128))
    auth_token = db.Column(db.String(36), nullable = True)
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)

    def set_auth_token(self,token):
        self.auth_token = token

    def getCredentials(self):
        return {
                "fullname" : self.fullname , 
                "email" : self.email
            }
    
class Student(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(120) ,index=True,unique=True, nullable = False)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(100))
    phone = db.Column(db.String(10), unique = True, nullable = True)
    photo = db.Column(db.LargeBinary, nullable = True)
    resume = db.Column(db.LargeBinary, nullable = True)
    rollno = db.Column(db.String(10), unique = True, nullable = True)
    course = db.Column(db.String(128), nullable = True)
    auth_token = db.Column(db.String(36), nullable = True)
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)

    def set_auth_token(self,token):
        self.auth_token = token

    def getCredentials(self):
        return {
            "fullname" : self.fullname , 
    def getJsonData(self):
        data =  {
            "id": self.id,
            "name": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "rollno": self.rollno,
            "course": self.course
        }
        if self.photo is not None:
            data["photo"] = True
        else:
            data["photo"] = False
        if self.resume is not None:
            data["resume"] = True
        else:
            data["resume"] = False
        "email" : self.email
        }
    
    
    def setPhoto(self, image):
        self.photo = image
    
    def getPhoto(self):
        return({"image": self.photo})
    
    def setResume(self, res):
        self.resume = res
    
    def getResume(self):
        return({"resume": self.resume})

    

class Company(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(120) ,index=True,unique=True, nullable = False)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128) ,index=True,unique=True, nullable = False)
    phone = db.Column(db.String(10), index = True, unique = True, nullable = True)
    logo = db.Column(db.LargeBinary, nullable = True)
    website = db.Column(db.String(128), nullable = False)
    auth_token = db.Column(db.String(36), nullable = True)
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)

    def set_auth_token(self,token):
        self.auth_token = token
    ########### UPLOAD LOGO
    ##### EDIT DETAILS
    def getCredentials(self):
        return {
                "fullname" : self.fullname , 
                "email" : self.email
                }

class Event(db.Model):
    id = db.Column(db.Integer , primary_key=True)

    name = db.Column(db.String(64) ,index=True)
    event_type = db.Column(db.String(16) ,index=True, nullable = False)
    poster = db.Column(db.LargeBinary, nullable = True)
    content = db.Column(db.String(512), nullable = False)
    reg_form = db.Column(db.String(128), nullable = True)
    posted_by = db.Column(db.String(128), nullable = False)
    organizer = db.Column(db.String(128), nullable = False)
    last_date = db.Column(db.Date, nullable = False)
    event_date = db.Column(db.Date, nullable = False)
    venue = db.Column(db.String, nullable = True)

    def getJsonData(self):
        return {
                "id": self.id,
                "name" : self.name , 
                "type": self.event_type,
                "poster": self.poster,
                "content": self.content,
                "form_link": self.reg_form,
                "posted_by": self.posted_by,
                "organizer": self.organizer,
                "last_date": self.last_date,
                "event_date": self.event_date,
                "venue": self.venue
                }


class Registrations(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    student_id = db.Column(db.Integer, nullable = False)
    event_id =  db.Column(db.Integer , nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)

    def register(eventid, userid):
        self.event_id = eventid
        self.student_id = userid
        self.timestamp = datetime.datetime()