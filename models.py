from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class HeadHunterVacancy(Base):
    __tablename__ = 'head_car_devices'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    salary: Mapped[int]
    link: Mapped[str]

    @property
    def repr(self) -> str:
        return f'HeadHunterVacancy(id={self.id!r}, name={self.name!r}, location={self.salary!r}, description={self.link!r})'


engine = create_engine('sqlite:///wires_devices.db', echo=True)
Base.metadata.create_all(engine)
