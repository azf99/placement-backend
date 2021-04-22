import os 
from app import app , databasePath , db
from models import Admin
#if not os.path.exists(databasePath):
#    db.create_all() 


db.create_all()

EMAIL = "azfar@gmail.com"
PASSWORD = "azfar@123"
PHONE = "6388528132"
NAME = "Azfar Lari"
superuser = Admin()
superuser.email = EMAIL 
superuser.phone = PHONE
superuser.fullname = NAME
superuser.set_password(PASSWORD) 

db.session.add(superuser)
db.session.commit() 

app.run(debug=True)
