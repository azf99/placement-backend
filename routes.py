
from uuid import uuid4
from datetime import datetime
import base64
from flask import Flask , request , jsonify
from app import app , db
from models import Student, Company, Admin, Event, Registrations

def check_token(token, user):
    if user is None:
        msg = {
                "status" : { 
                    "type" : "failure" ,   
                    "message" : "Unauthorized Token"
                    }
                }
        return(msg)
    return(True)

def verify_admin(token):
    user = Admin.query.filter_by(auth_token=token).first() 
    if user is None:
        msg = {
                "status" : { 
                    "type" : "failure" ,   
                    "message" : "Unauthorized Token"
                    }
                }
        return(msg)
    return(True)

@app.route('/test') 
def home():
    return jsonify({"status": "success"})


@app.route('/API/login', methods=['POST'])
def login():
    AUTHS = ["Admin", "Student", "Company"]
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('type')

    msg = ""
    if not email or not password or (user_type not in AUTHS): 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "Missing Data"
                }
            }
        return jsonify(msg)
    
    if user_type == "Student":
        user = Student.query.filter_by(email=email).first() 
        if user is None or not user.check_password(password) :
            msg = {
                    "status" : { 
                        "type" : "failure" ,   
                        "message" : "Username or password incorrect"
                        }
                    }
        else:
            token = str(uuid4())
            user.set_auth_token(token)
            db.session.add(user)
            db.session.commit()
            msg = {
                    "status" : { 
                        "type" : "success" ,
                        "message" : "You logged in"
                        } , 
                    "data" : {
                    "user" : user.getCredentials()
                    },
                    "token": token
            }
    elif user_type == "Company":
        user = Company.query.filter_by(email=email).first() 
        if user is None or not user.check_password(password) :
            msg = {
                    "status" : { 
                        "type" : "failure" ,   
                        "message" : "Username or password incorrect"
                        }
                    }
        else:
            token = str(uuid4())
            user.set_auth_token(token)
            db.session.add(user)
            db.session.commit()
            msg = {
                    "status" : { 
                        "type" : "success" ,
                        "message" : "You logged in"
                        } , 
                    "data" : {
                    "user" : user.getCredentials()
                    },
                    "token": token
            }
    elif user_type == "Admin":
        user = Admin.query.filter_by(email=email).first() 
        if user is None or not user.check_password(password) :
            msg = {
                    "status" : { 
                        "type" : "failure" ,   
                        "message" : "Username or password incorrect"
                        }
                    }
        else:
            token = str(uuid4())
            user.set_auth_token(token)
            db.session.add(user)
            db.session.commit()
            msg = {
                    "status" : { 
                        "type" : "success" ,
                        "message" : "You logged in"
                        } , 
                    "data" : {
                    "user" : user.getCredentials()
                    },
                    "token": token
            }

    return jsonify(msg)

@app.route('/API/register', methods=['POST'])
def register():
    AUTHS = ["Admin", "Student", "Company"]
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    user_type = request.form.get('type')
    token = request.form.get('token')

    auth = verify_admin(token)

    if auth != True:
        return(auth)

    msg = ""
    if not password or not email or (user_type not in AUTHS): 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg)
    
    if user_type == "Student":
        if Student.query.filter_by(email=email).count() == 1 : 
            msg = {
                "status" : { 
                    "type" : "failure" ,   
                    "message" : "email already taken"
                    }
                }
            return jsonify(msg)
        
        u = Student()
        u.fullname = fullname
        u.email = email 
        u.set_password(password) 

        db.session.add(u)
        db.session.commit() 
    elif user_type == "Company":
        if Company.query.filter_by(email=email).count() == 1 : 
            msg = {
                "status" : { 
                    "type" : "failure" ,   
                    "message" : "email already taken"
                    }
                }
            return jsonify(msg)
        
        phone = request.form.get('phone')
        website = request.form.get('website')
        name = request.form.get('name')
        u = Company()
        u.website = website
        u.phone = phone
        u.email = email 
        u.fullname = name
        u.set_password(password) 

        db.session.add(u)
        db.session.commit() 
    elif user_type == "Admin":
        if Admin.query.filter_by(email=email).count() == 1 : 
            msg = {
                "status" : { 
                    "type" : "failure" ,   
                    "message" : "email already taken"
                    }
                }
            return jsonify(msg)
        phone = request.form.get('phone')
        name = request.form.get('name')
        u = Admin()
        u.email = email 
        u.phone = phone
        u.fullname = name
        u.set_password(password) 

        db.session.add(u)
        db.session.commit() 
    
    msg = {
            "status" : { 
                "type" : "success" ,   
                "message" : "You have registered"
                }
            }
    return jsonify(msg)

@app.route('/API/change_password', methods=['POST'])
def change_password():
    AUTHS = ["Admin", "Student", "Company"]
    oldpassword = request.form.get('old_password')
    newpassword = request.form.get('new_password')
    email = request.form.get('email')
    user_type = request.form.get('type')
    msg = ""
    if not oldpassword or not email or (user_type not in AUTHS): 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg)
    if user_type == "Student":
        user = Student.query.filter_by(email=email).first() 
        if user is None or not user.check_password(oldpassword) :
            msg = {
                    "status" : { 
                        "type" : "failure" ,   
                        "message" : "Username or password incorrect"
                        }
                    }
        else:
            user.set_password(newpassword)
            db.session.commit()
            msg = {
                "status" : { 
                    "type" : "success" ,
                    "message" : "Password changed Successfully"
                    } ,                 "data" : {
                "user" : user.getCredentials()
                }
            }
    elif user_type == "Company":
        user = Company.query.filter_by(email=email).first() 
        if user is None or not user.check_password(oldpassword) :
            msg = {
                    "status" : { 
                        "type" : "failure" ,   
                        "message" : "Username or password incorrect"
                        }
                    }
        else:
            user.set_password(newpassword)
            db.session.commit()
            msg = {
                "status" : { 
                    "type" : "success" ,
                    "message" : "Password changed Successfully"
                    } ,                 "data" : {
                "user" : user.getCredentials()
                }
            }
    elif user_type == "Admin":
        user = Admin.query.filter_by(email=email).first() 
        if user is None or not user.check_password(oldpassword) :
            msg = {
                    "status" : { 
                        "type" : "failure" ,   
                        "message" : "Username or password incorrect"
                        }
                    }
        else:
            user.set_password(newpassword)
            db.session.commit()
            msg = {
                "status" : { 
                    "type" : "success" ,
                    "message" : "Password changed Successfully"
                    } ,                 "data" : {
                "user" : user.getCredentials()
                }
            }
    return jsonify(msg)

@app.route('/API/download_photo', methods=['POST'])
def down_photo():
    token = request.form.get('token')
    msg = ""
    if not token : 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg)
    user = Student.query.filter_by(auth_token=token).first() 
    auth = check_token(token, user)
    if auth == True:
        msg = user.getPhoto()
    else:
        return(auth)

    return jsonify(msg)

@app.route('/API/add_event', methods=['POST'])
def add_event():
    AUTHS = ["Admin", "Student", "Company"]
    token = request.form.get('token')
    user_type = request.form.get('type')
    msg = ""
    if not token and user_type not in AUTHS: 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg)
    name = request.form.get('name')
    event_type = request.form.get('event_type')
    poster = request.form.get('poster')   ######### Diffwrebt API
    content = request.form.get('content')
    reg_form = request.form.get('form')
    organizer = request.form.get('organizer')
    last_date = request.form.get('last_date')
    event_date = request.form.get('event_date')
    venue = request.form.get('venue')

    event = Event()
    event.name = name
    event.event_type = event_type
    event.content = content
    event.poster = poster
    event.reg_form = reg_form
    event.organizer = organizer
    event.last_date = datetime.strptime(last_date, "%Y-%m-%d")
    event.event_date = datetime.strptime(event_date, "%Y-%m-%d")
    event.venue = venue
    if user_type == "Student":
        user = Student.query.filter_by(auth_token=token).first() 
        auth = check_token(token, user)
        if auth == True:
            event.posted_by = user.fullname
        else:
            return(auth)
    elif user_type == "Company":
        user = Company.query.filter_by(auth_token=token).first() 
        auth = check_token(token, user)
        if auth == True:
            event.organizer = user.fullname
            event.posted_by = user.fullname
        else:
            return(auth)
    elif user_type == "Admin":
        user = Admin.query.filter_by(auth_token=token).first() 
        auth = check_token(token, user)
        if auth == True:
            event.posted_by = user.fullname
        else:
            return(auth)
    db.session.add(event)
    db.session.commit()
    return jsonify({
            "status" : { 
                "type" : "success" ,   
                "message" : "Event Added Successfully"
                }
            })

@app.route('/API/add_profile', methods=['POST'])
def add_profile():
    AUTHS = ["Student"]
    token = request.form.get('token')
    user_type = request.form.get('type')
    msg = ""
    if not token and user_type not in AUTHS: 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg) 
    user = Student.query.filter_by(auth_token=token).first() 
    auth = check_token(token, user)
    token = request.form.get('fullname')
    phone = request.form.get('phone')
    rollno = request.form.get('rollno')
    course = request.form.get('course')
    
    user.rollno = rollno
    user.phone = phone
    user.course = course
    db.session.commit()
    return jsonify({
        "status": {
            "type": "success",
            "message": "profile updated successfully"
        }
    })

@app.route('/API/get_event_list', methods=['POST'])
def get_event_list():
    AUTHS = ["Admin", "Student", "Company"]
    token = request.form.get('token')
    user_type = request.form.get('type')
    msg = ""
    if not token and user_type not in AUTHS: 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg) 
    user = Student.query.filter_by(auth_token=token).first() 
    auth = check_token(token, user)
    if auth != True:
        return jsonify(auth)
    date = datetime.now()
    today = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    today = datetime.strptime(today, '%Y-%m-%d')
    x = db.session.query(Event).filter(Event.event_date < today).all()
    completed = []
    for i in x:
        completed.append(i.getJsonData())
    x = db.session.query(Event).filter(Event.event_date > today).all()
    upcoming = []
    for i in x:
        completed.append(i.getJsonData())
    
    return jsonify({
        "events": 
            {
                "upcoming": upcoming,
                "completed": completed
            }
        })

@app.route('/API/get_poster', methods=['GET', 'POST'])
def get_poster():
    AUTHS = ["Admin", "Student", "Company"]
    token = request.form.get('token')
    get_id = request.form.get('id')
    user_type = request.form.get('type')
    msg = ""
    if not token and user_type not in AUTHS: 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg) 
    user = Student.query.filter_by(auth_token=token).first() 
    auth = check_token(token, user)
    if auth != True:
        return jsonify(auth)
    x = db.session.query(Event).filter(Event.id == get_id).first()
    if x is None:
        msg = {
            "status": {
                "type": "failure",
                "message": "id does not exist"
            }
        }
    
    img = x.get_poster()
    msg = {
        "status": {
            "type": "success",
            "message": "id does not exist"
        }
        "image": img
    }
    return jsonify(msg)

@app.route('/API/register_event', methods=['POST'])
def register_event():
    def check_registration(eventid, userid):
        res = db.session.query(Registrations).filter(Registrations.event_id == eventid, Registrations.student_id == userid).first()
        if res is not None:
            return True
        else:
            return False
    
    AUTHS = ["Student"]
    token = request.form.get('token')
    user_type = request.form.get('type')
    msg = ""
    if not token and user_type not in AUTHS: 
        msg = {
            "status" : { 
                "type" : "failure" ,   
                "message" : "missing data"
                }
            }
        return jsonify(msg) 
    user = Student.query.filter_by(auth_token=token).first() 
    auth = check_token(token, user)

    event_id = request.form.get('event_id')
    reg = Registrations()
    if check_registration(event_id, user.id):
        return jsonify({
            "status": {
                "type": "success",
                "message": "Already Registered"
            }
        })
    reg.register(event_id, user.id)
    db.session.add(reg)
    db.session.commit()
    return jsonify({
            "status": {
                "type": "success",
                "message": "Registration Done Successfully"
            }
        })

