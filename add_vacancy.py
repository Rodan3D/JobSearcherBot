from sqlalchemy.orm import Session
from models import engine

from models import HeadHunterVacancy

with Session(engine) as session:
    dev1 = HeadHunterVacancy(
        name='БК',
        location='шкаф №1',
        description='Батарейный контактор.'
    )

    # session.add_all([dev1])
    # session.commit()
from sqlalchemy import select

session = Session(engine)

stmt = select(HeadHunterVacancy).where(HeadHunterVacancy.name.in_(["ПР-55"]))

res = session.scalar(stmt).description
print(res)

# for device in session.scalars(stmt):
#     print(device.description)