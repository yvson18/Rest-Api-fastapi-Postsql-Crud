"""coded by Yvson following Building a REST API in FastAPI + PostgreSQL - Users CRUD in 23 Minutes tutorial
"""

from fastapi import FastAPI
import databases,sqlalchemy

##-------------------------Postgres Database-----------------------------------
usuario_posgre = "usertest"
senha = "usertest222"
ip = "localhost" # deixa localhost para ficar nao dar ruim
porta = "5432"

DATABASE_URL = f"postgresql://{usuario_posgre}:{senha}@{ip}:{porta}/dbtest"
database = databases.Database(DATABASE_URL) #Acho que se usa a url para fazer as devidas conexoes com o banco
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id"          , sqlalchemy.String,primary_key= True),
    sqlalchemy.Column("username"    ,sqlalchemy.String),
    sqlalchemy.Column("password"    ,sqlalchemy.String),
    sqlalchemy.Column("password"    ,sqlalchemy.String),
    sqlalchemy.Column("first_name"  ,sqlalchemy.String),
    sqlalchemy.Column("last_name"   ,sqlalchemy.String),
    sqlalchemy.Column("gender"      ,sqlalchemy.CHAR),
    sqlalchemy.Column("last_name"   ,sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)


##-----------------------------------------------------------------------------


app = FastAPI()


@app.get("/users")
def find_all_user():
    return "List all user"

    