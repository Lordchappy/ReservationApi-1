from fastapi import HTTPException, status, Depends,Response
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from fastapi.security.oauth2 import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from ..services import auth
from fastapi_utils.inferring_router import InferringRouter
from ..models import schemas,models
from ..database import get_db
from ..services import utils
from typing import Optional,List
auth_handler = auth.Auth()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

router = InferringRouter(prefix ="/users", tags=["Users"]) 
@cbv(router)
class Users:
    db:Session=Depends(get_db)

    def get_current_user(token: str = Depends(oauth2_scheme),db : Session = Depends(get_db))-> schemas.UserOutput:
        token_data = auth_handler.decode_token(token)
        user = db.query(models.User).filter(models.User.id == token_data).first()
        return user

    @router.get('/all',response_model=List[schemas.UserOutput],status_code=status.HTTP_200_OK)
    async def get_all_users(self)-> schemas.UserOutput:
        users = self.db.query(models.User).all()
        if users:
            return users
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "No user present in database")

    @router.post('/email',response_model=schemas.UserOutput,status_code=status.HTTP_200_OK)
    async def get_user_by_email(self,email:str) -> schemas.UserOutput:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"User with email {email} does not exists ")
        return user

    @router.post('/username',response_model=schemas.UserOutput,status_code=status.HTTP_200_OK)
    async def get_user_by_username(self,username:str) -> schemas.UserOutput:
        user =  self.db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"User with username {username} does not exists ")
        return user

    @router.get('/{id}',response_model=schemas.UserOutput,status_code=status.HTTP_200_OK)
    async def get_user_by_id(self,id:int)-> schemas.UserOutput:
        user = self.db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"user with id number {id} does not exist")
        return user

    @router.post('/signup',response_model=schemas.UserOutput,status_code=status.HTTP_201_CREATED)
    async def create_user(self, user:schemas.UserCreate)-> schemas.UserOutput:
        username =  self.db.query(models.User).filter(models.User.username == user.username).first()
        if username:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"User with username {user.username} already exists")
        email =  self.db.query(models.User).filter(models.User.email == user.email).first()
        # email =  self.get_user_by_email(email=user.email)
        if email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"User with email {user.email} already exists")
        try:
            hashed_password = utils.hash(user.password)
            user.password = hashed_password
            new_user= models.User(**user.dict())
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as err:
            return {"message" : err}

    @router.post('/login',response_model=schemas.Token,status_code=status.HTTP_202_ACCEPTED)
    async def login(self, user_credentials: OAuth2PasswordRequestForm = Depends())-> schemas.Token:
        user = self.db.query(models.User).filter(models.User.email == user_credentials.username).first()
        print (user)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
        access_token = auth_handler.encode_token(user.id)
        return {"access_token": access_token, "token_type": "bearer"}

    @router.post('/update',response_model=schemas.UserOutput,status_code=status.HTTP_202_ACCEPTED)
    async def update_user(self,first_name: Optional[str],last_name: Optional[str],current_user: int= Depends(get_current_user)):
        # user =  self.get_user_by_id(id=current_user.id)
        user = self.db.query(models.User).filter(models.User.id == current_user.id).first()
        if user:
            try:
                user.first_name = first_name or user.first_name
                user.last_name = last_name or user.last_name
                self.db.commit()
                self.db.refresh(user)
                return user
            except Exception as err:
                return {"message" : err}


    @router.delete('/delete',status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(self,current_user: int= Depends(get_current_user)):
        # user = self.get_user_by_id(id=id)
        user = self.db.query(models.User).filter(models.User.id == current_user.id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "user not found")
        user.delete(synchronize_session=False)
        self.db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)




                
  
            

           
        
