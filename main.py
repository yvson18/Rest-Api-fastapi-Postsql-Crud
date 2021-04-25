from fast api import FastAPI

app = FastAPI()


@app.get("/users")
def find_all_user():
    return "List all user"