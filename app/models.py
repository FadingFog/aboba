from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class BaseA(Base):
    __abstract__ = True


class BaseB(Base):
    __abstract__ = True


class SomeDataA(BaseA):
    __tablename__ = 'some_data'

    name: Mapped[str] = mapped_column(String(255))


class SomeDataB(BaseB):
    __tablename__ = 'some_data'

    name: Mapped[str] = mapped_column(String(255))
