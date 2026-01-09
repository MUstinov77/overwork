from sqlalchemy import delete, select, update
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
