from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Boolean
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    name: Mapped[str] = mapped_column(String(64))
    login: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(1024))
    avatar: Mapped[str] = mapped_column(String(16384))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, login={self.login!r})"

class Series(Base):
    __tablename__ = "series"
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    name: Mapped[str] = mapped_column(String(64))
    books: Mapped[List["Book"]] = relationship(back_populates="series")

    def __repr__(self) -> str:
        return f"Series(id={self.id!r}, name={self.name!r})"

class Publisher(Base):
    __tablename__ = "publishers"
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    name: Mapped[str] = mapped_column(String(128))
    color: Mapped[str] = mapped_column(String(8))
    books: Mapped[List["Book"]] = relationship(back_populates="publisher")

    def __repr__(self) -> str:
        return f"Publisher(id={self.id!r}, name={self.name!r})"

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    title: Mapped[str] = mapped_column(String(128))
    author: Mapped[str] = mapped_column(String(128))
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"))
    series: Mapped["Series"] = relationship("Series", back_populates="books")
    pages: Mapped[int] = mapped_column(Integer)
    cover: Mapped[bool] = mapped_column(Boolean)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="books")


    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r})"