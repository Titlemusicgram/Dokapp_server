from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
