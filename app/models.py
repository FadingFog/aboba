from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


# Declare DeclarativeBases & Models for each engine (data source)
# according to https://docs.sqlalchemy.org/en/20/orm/persistence_techniques.html#session-partitioning

class BaseA(Base, DeclarativeBase):
    __abstract__ = True


class BaseB(Base, DeclarativeBase):
    __abstract__ = True


class BaseC(Base, DeclarativeBase):
    __abstract__ = True


class SomeDataCommon:
    name: Mapped[str] = mapped_column(String(255))


class SomeDataA(SomeDataCommon, BaseA):
    __tablename__ = 'some_data'


class SomeDataB(SomeDataCommon, BaseB):
    __tablename__ = 'some_data2'


class SomeDataC(SomeDataCommon, BaseC):
    __tablename__ = 'some_data3'
