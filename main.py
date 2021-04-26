"""coded by Yvson following Building a REST API in FastAPI + PostgreSQL - Users CRUD in 23 Minutes tutorial
"""
import databases
import sqlalchemy
import datetime
import uuid
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

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
    sqlalchemy.Column("first_name"  ,sqlalchemy.String),
    sqlalchemy.Column("last_name"   ,sqlalchemy.String),
    sqlalchemy.Column("gender"      ,sqlalchemy.CHAR),
    sqlalchemy.Column("create_at"   ,sqlalchemy.String),
    sqlalchemy.Column("status"      ,sqlalchemy.CHAR),
)

engine = sqlalchemy.create_engine(DATABASE_URL) # The Engine is the starting point for any SQLAlchemy application.

metadata.create_all(engine)

##-------------------------------Models----------------------------------------

class UserList(BaseModel):
    id: str
    username: str
    password: str
    first_name: str
    last_name: str
    gender: str
    create_at: str
    status: str

app = FastAPI()

class UserEntry(BaseModel):
    username: str = Field(...,exmaple="Mago Implacavel")
    password: str = Field(...,exmaple="mage1337")
    first_name: str = Field(...,exmaple="Mago")
    last_name: str = Field(...,exmaple="Cinzento")
    gender: str = Field(...,exmaple="M")

class UserUpdate(BaseModel):
    id        : str = Field(..., example="Enter your id")
    first_name: str = Field(..., example="Mago")
    last_name : str = Field(..., example="Cinzento")
    gender    : str = Field(..., example="M")
    status    : str = Field(..., example="1")

class UserDelete(BaseModel):
    id:str = Field(...,example="Enter your id")


#-----------------------Pesquisar sobre o on_event--------------------------

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users",response_model=List[UserList])
async def find_all_user():

    query = users.select()

    return await database.fetch_all(query)

@app.get("/users/{user_Id}",response_model=UserList)
async def find_user_by_id(user_Id: str):
    query = users.select().where(users.c.id == user_Id)
    return await database.fetch_one(query)



@app.post("/users",response_model=UserList)
async def find_all_user(user: UserEntry):

    gID = str(uuid.uuid1())
    gDate = str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username = user.username,
        password = user.password,
        first_name = user.first_name,
        last_name = user.last_name,
        gender = user.gender,
        create_at = gDate,
        status = "1"
    )

    await database.execute(query)

    return {
        "id":gID,
        **user.dict(),
        "create_at": gDate,
        "status": "1"
    }

@app.put("/users",response_model=UserList)
async def update_user(user: UserUpdate):
    
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name = user.last_name,
            gender = user.gender,
            status = user.status,
            create_at = gDate,
        )
    await database.execute(query)
    return await find_user_by_id(user.id)

@app.delete("/users/{userId}", tags=["Users"])
async def delete_user(user: UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This user has been deleted successfully." 
    }