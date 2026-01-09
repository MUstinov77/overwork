from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class BaseService:

    def __init__(self, session, model):
        self.session: Session = session
        self.model = model

    async def create(self, values: dict):
        record = self.model(**values)
        self.session.add(record)
        self.session.commit()
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
        query = delete(self.model).where(self.model.id == obj_id).returning(self.model)
        result = self.session.execute(query)
        return result.scalars().one()

    async def retrieve(self, obj_id: int):
        query = select(self.model).where(self.model.id == obj_id)
        result = self.session.execute(query)
        return result.scalars().one()

    async def create_instance(self, values: dict):
        try:
            record = await self.create(values)
            self.session.commit()
            return record
        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while creating instance",
            )

    async def delete_instance(self, obj_id: int):
        try:
            record = await self.delete(obj_id)
            self.session.commit()
            return record
        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while deleting instance",
            )


    async def update_instance(self, values: dict, obj_id :int):
        try:
            record = await self.update(values, obj_id)
            self.session.commit()
            return record
        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while updating instance"
            )
