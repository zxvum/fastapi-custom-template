from fastapi import Depends, FastAPI

from app import exceptions
from app.apps.auth.base_config import fastapi_users, auth_backend
from app.apps.auth.schemas import UserRead, UserCreate
from app.config import settings
from app.db.deps import set_db
from app.db.exceptions import DatabaseValidationError

from app.apps.chat.views import router as chat_router

app = FastAPI(
    title=settings.SERVICE_NAME,
    debug=settings.DEBUG,
    dependencies=[Depends(set_db)]
)

app.add_exception_handler(
    DatabaseValidationError,
    exceptions.database_validation_exception_handler
)

# app.include_router(chat_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get('/')
def index():
    return {"msg": "hegll"}
