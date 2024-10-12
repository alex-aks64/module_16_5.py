
from fastapi import FastAPI, Path, Request, Body,HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()


users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def root(request: Request)-> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "title": "Users"})


@app.get("/users/{user_id}")
async def get_users(request: Request, user_id: int)-> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html",
                                              {"request": request, "user": user, "title": f"User {user_id}"})
    raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
async def create_user(username: str = Path(..., example="User"), age: int = Path(..., example=28)):
    user = User(id=len(users) + 1, username=username, age=age)
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int = Path(...), username: str = Path(..., example="UpdateUser"),
                      age: int = Path(..., example=100)):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int = Path(...)):
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.on_event("startup")
async def create_users():
    await create_user("UrbanUser", 24)
    await create_user("UrbanTest", 22)
    await create_user("Capybara", 60)