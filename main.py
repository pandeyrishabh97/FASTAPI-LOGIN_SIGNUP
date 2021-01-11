import uvicorn
from fastapi import FastAPI
import py_functions
import config
import pyodbc
import json
import pywhatkit

app = FastAPI()


def connect_db(pwd):
    driver = config.DRIVER
    server = config.SERVER
    database = config.DATABASE
    uid = config.UID
    pwd = pwd
    trust = config.TRUST
    con_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}'
    cnxn = pyodbc.connect(con_string)
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    print("Connection Successful With DataBase")
    return cnxn,cursor


with open('SQL/password.json') as f:
    # {"password": "xyz"}
    data = json.load(f)
pwd=data['password']

cnxn,cursor = connect_db(pwd)


@app.get('/')
def get_data(search:str = ""):
    df = py_functions.fetch_data(search,cnxn)
    return df.to_dict('r')


@app.post('/search/')
def search_video(search:str):
    pywhatkit.playonyt(str(search))


@app.post('/signup/')
def signup(firstname: str,lastname:str,city:str,email:str,password:str):
    if '@' not in email:
        return {"Email ID Invalid"}
    if len(password)<5 or "#" not in password:
        return {"Password is not secure please input 6 digit password and add # for more security"}
    user_exist = py_functions.check_user_exist(email,cnxn)
    if user_exist==0:
        signup_query = py_functions.signup_data(firstname,lastname,city,email,password)
        cursor.execute(signup_query)
        return {"status":"Signed Up Please login with same creds."}
    else:
        return {"status":'Email ID already exist.'}


@app.post('/login/')
def login(email: str,password:str):
    user_exist = py_functions.check_user_details(email,password,cnxn)
    if user_exist>0:
        return {"Status":"Login Successful Access Granted"}
    else:
        return {"Status":"Login error Access not Granted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
