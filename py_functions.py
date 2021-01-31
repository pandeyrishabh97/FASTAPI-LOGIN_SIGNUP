import pandas as pd
from random import randint
import config
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def fetch_data(search,cnxn):
    query_cols='select top 1* from SALES_DATA'
    df=pd.read_sql(query_cols,cnxn)
    # col_list=df.columns.tolist()
    col_list=(",".join(df.columns))
    print(col_list)
    query = 'SELECT TOP 10* FROM SALES_DATA '\
            "where lower(concat("+col_list+")) like '%"+search+"%'"
    print(query)
    df = pd.read_sql(query,cnxn)
    return df


def check_user_details(username,password,cnxn):
    query = 'select * from USER_CREDS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
    df= pd.read_sql(query,cnxn)
    return df.shape[0]


def check_user_exist(email,cnxn):
    query = 'select * from USER_CREDS where email='+"'"+str(email)+"'"
    df= pd.read_sql(query,cnxn)
    return df.shape[0]


def signup_data(firstname,lastname,city,email,password):
    query = "INSERT INTO USER_CREDS "\
            "VALUES ("+"'"+str(firstname)+"'"+",'"+str(lastname)+"'"+",'"+str(city)+"'"+"" \
            ",'"+str(email)+"','"+str(password)+"'"+")"
    print(query)
    return query

def generate_code():
    return randint(100000,1000000)

def send_auth_code(email,cursor):
    code = generate_code()
    query="UPDATE USER_CRED SET PASSCODE ="+str(code)+"where EMAIL='"+str(email)+"'"
    cursor.execute(query)
    return code


def generate_auth_email(passcode,RECEIVER_EMAIL):
    subject = "Verification Code"
    body ="\nHi Everyone,\n\n Your verification code is "+str(passcode)
    sender_email = config.EMAIL_ID
    receiver_email = RECEIVER_EMAIL
    password = config.EMAIL_PWD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def generate_password_change_email(RECEIVER_EMAIL):
    subject = "URGENT: Password Change"
    body ="\nHi User,\n\n Your password changed successfully "
    sender_email = config.EMAIL_ID
    receiver_email = RECEIVER_EMAIL
    password = config.EMAIL_PWD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def validate_passcode(email,passcode,cnxn):
    query = "select * from USER_CRED WHERE EMAIL='"+str(email)+"' AND PASSCODE = "+str(passcode)
    df=pd.read_sql(query,cnxn)
    if df.shape[0]>0:
        return True
    else:
        return False

def update_password(email,password,cursor):
    query = "UPDATE USER_CRED SET PASSWORD ='" + str(password) + "' where EMAIL='" + str(email) + "'"
    cursor.execute(query)



















