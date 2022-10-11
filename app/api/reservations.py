from tkinter import CURRENT
from fastapi import HTTPException, status, Depends,Response
from sqlalchemy.orm import Session
from ..services import auth
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from ..models import schemas,models
from ..database import get_db
from ..services import utils
from typing import Optional,List
from .users import Users
MAX_ROOM_NUMBERS = 250
router = InferringRouter(prefix ="/reservations", tags=["Reservations"]) 
@cbv(router)
class Reservations:
    db:Session=Depends(get_db)

    @router.get("/all", response_model=List[schemas.Reservations_Output],status_code=status.HTTP_200_OK)
    async def get_all_reservations(self)-> schemas.Reservations_Output:
        rental =  self.db.query(models.Reservations).all()
        if not rental:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not present")
        return rental

    @router.get("/{id}", response_model=schemas.Reservations_Output,status_code=status.HTTP_200_OK)
    async def get_rentals_with_id(self,id:int)-> schemas.Reservations_Output:
        rental =  self.db.query(models.Reservations).filter(models.Reservations.id == id).first()
        if not rental:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Rental with id number {id} does not exist")
        return rental

    @router.post("/room", response_model=schemas.Reservations_Output,status_code=status.HTTP_200_OK)
    async def get_rentals_with_room_number(self,room_number:int) -> schemas.Reservations_Output:
        rental = self.db.query(models.Reservations).filter(models.Reservations.Room_number == room_number).first()
        if not rental:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Room {room_number} is not occupied")
        return rental

    @router.post("/new_reservations", response_model=schemas.Reservations_Output,status_code=status.HTTP_201_CREATED)
    async def new_rentals(self,rental:schemas.Reservations,current_user: int= Depends(Users.get_current_user))-> schemas.Reservations_Output:
        rentals =  self.db.query(models.Reservations).filter(models.Reservations.Room_number == rental.Room_number).first()
        if rentals:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Occupied")
        if rental.Room_number >= MAX_ROOM_NUMBERS:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Room not available")
        new_rental = models.Reservations(owner_id=current_user.id,**rental.dict(),is_active=True)
        self.db.add(new_rental)
        self.db.commit()
        self.db.refresh(new_rental)
        return new_rental

    @router.post("/update/{id}", response_model=schemas.Reservations_Output,status_code=status.HTTP_202_ACCEPTED)
    async def update_rentals(self,id: int,booking_time: str,current_user: int= Depends(Users.get_current_user))-> schemas.Reservations_Output:
        rental =  self.db.query(models.Reservations).filter(models.Reservations.id == id).first()
        if rental:
            try:
                rental.booking_time = booking_time
                self.db.commit()
                self.db.refresh(rental)
                return rental
            except Exception as err:
                return {"message" : err}

    # @router.get("/rentals", response_model=List[schemas.Reservations_Output],status_code=status.HTTP_200_OK)
    # async def get_users_reservations(self,current_user: int= Depends(Users.get_current_user))-> schemas.Reservations_Output:
        
    #     rental =  self.db.query(models.Reservations).filter(models.Reservations.owner_id == .first()
    #     if not rental:
    #          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not present")
    #     return rental
    
    @router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
    async def delete_rentals(self,id:int,current_user: int= Depends(Users.get_current_user)):
        rental = self.db.query(models.Reservations).filter(models.Reservations.id== id)
        if not rental.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "user not found")
        rental.delete(synchronize_session=False)
        self.db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)



