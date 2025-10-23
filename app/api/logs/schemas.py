from datetime import datetime

from pydantic import BaseModel

from app.core.enum import LogType


class LogCreate(BaseModel):
    type: LogType