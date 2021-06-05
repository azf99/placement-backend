
from flask import Flask , request , jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__) 

CORS(app)

currentDirectory = os.getcwd() 
databasePath = os.path.join(currentDirectory , "database.db")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://vxdchuphjsryxr:8980947f072b81ab8109c1947e4f2fafda83d275dc02ca5ecb0b2e23c13740a5@ec2-184-73-198-174.compute-1.amazonaws.com:5432/d650arrdb8bgtn"
db = SQLAlchemy(app) 

import routes , models 

if __name__ == "__main__":
    app.run(threaded = True)