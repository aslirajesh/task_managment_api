from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import models, schemas, crud, auth, database
from .schemas import LoginForm

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return crud.create_user(db=db, user=user)


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: LoginForm, db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(
        db,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)


@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    tasks = crud.get_tasks(db=db, user_id=current_user.id)
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    task = crud.get_task(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    updated_task = crud.update_task(
        db=db,
        task=task,
        task_id=task_id,
        user_id=current_user.id
    )
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    deleted_task = crud.delete_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
