from fastapi import Depends, FastAPI

from app import exceptions
from app.config import settings
from app.db.deps import set_db
from app.db.exceptions import DatabaseValidationError

app = FastAPI(
    title=settings.SERVICE_NAME,
    debug=settings.DEBUG,
    dependencies=[Depends(set_db)]
)

app.add_exception_handler(
    DatabaseValidationError,
    exceptions.database_validation_exception_handler
)

@app.get('/')
def index():
    return {"msg": "hegll"}