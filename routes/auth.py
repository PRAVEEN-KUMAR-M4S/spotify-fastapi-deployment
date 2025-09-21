
import uuid
import bcrypt
from fastapi import Depends, HTTPException, Header
from database import get_db
from middleware.auth_middle_ware import auth_middleware
from models.user import User
from pydantic_schema.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from pydantic_schema.user_login import UserLogin
import jwt


router=APIRouter()

@router.post('/signup',status_code=201)
def signup_user(user: UserCreate,db: Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email == user.email).first()

    if  db_user:
        raise HTTPException(400,"User with same email exists !")
       
    
    hashed_pwd=bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()) 
    
    db_user=User(id=str(uuid.uuid4()),email=user.email,password=hashed_pwd,name=user.name)
    
    db.add(db_user) 
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post('/login')
def login_user(user:UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email == user.email).first()

    if not db_user:
      raise HTTPException(400,"User not found please register !")
    
    is_match=bcrypt.checkpw(user.password.encode(),db_user.password)

    if not is_match:
        raise HTTPException(400,"Incorrect password !")
    
    token= jwt.encode({'id':db_user.id},'password_key')
    
    return {'user':db_user,'token':token}

@router.get('/')
def current_user_data(db: Session=Depends(get_db),user_dic=Depends(auth_middleware)):
    user=db.query(User).filter(User.id == user_dic['uid']).options(
        joinedload(User.favorite)
    ).first()
    if not user:
        raise HTTPException(404,"User not found") 
    
    return user
          

