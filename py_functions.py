import pandas as pd


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



























