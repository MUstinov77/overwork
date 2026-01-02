from typing import Any

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider




class BaseService:
    model = None

    def __init__(self, session, model):
        self.session = session
        self.model = model


    async def create(self, values):
        record = self.model(**values)
        self.session.add(record)
        return record

    async def update(self, values: dict, obj_id: int):
        query = (
            update(self.model).
            where(self.model.id == obj_id).
            values(**values).
            returning(self.model)
        )
        result = self.session.execute(query)
        return result.scalars().one()

    async def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id).returning(self.model)
        result = self.session.execute(query)
        return result.scalars().one()

    async def retrieve(self, obj_id: int):
        query = select(self.model).where(self.model.id == obj_id)
        result = self.session.execute(query)
        return result.scalars().one()



