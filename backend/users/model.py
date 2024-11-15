from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.db import Base
from backend.utils.vars import created_at, intpk, updated_at


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    pastes: Mapped[set["Paste"]] = relationship(back_populates="user")  # type: ignore # noqa: F821
