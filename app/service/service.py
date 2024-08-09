from sqlalchemy.orm import Session
from app.model.model import User as UserModel


# check existing users with username and email
async def exixting_user(db: Session, username: str, email:str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None


