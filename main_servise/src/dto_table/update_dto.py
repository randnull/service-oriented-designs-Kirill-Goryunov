from pydantic import BaseModel
import datetime
from typing import Optional


class UpdateModel(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[str] = None
    phone: Optional[str] = None
