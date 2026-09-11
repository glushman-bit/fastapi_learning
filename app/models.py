from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    """Класс модели User.  Отвечает за БД."""
    __tablename__ = 'users'

    __table_args__ = (
        UniqueConstraint('email', name='uq_users_email'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    age: Mapped[int]
