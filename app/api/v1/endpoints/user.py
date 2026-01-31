from fastapi import APIRouter, status
from app.schemas.user import UserResponse, UserUpdate, UserCreate, UserUpdateMe

router = APIRouter()

@router.get("/")
async def get_user_info():
    return {"message": "User information"}

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    return {"message": "Current user information"}

@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_current_user(data: UserUpdateMe):
    return {"message": "Current user updated", "data": data}

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate):
    return {"message": "User created", "data": data}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    pass

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, data: UserUpdate):
    return {"message": f"User with id {user_id} updated", "data": data}
