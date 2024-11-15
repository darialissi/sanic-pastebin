from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.db import Base
from backend.utils.vars import created_at, expired_at, intpk


class Paste(Base):
    __tablename__ = "pastes"

    id: Mapped[intpk]
    uri: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[created_at]
    expired_at: Mapped[expired_at]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="pastes")  # type: ignore # noqa: F821

    def to_dict(self):
        return {
            "id": self.id,
            "uri": self.uri,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "expired_at": self.expired_at.strftime("%Y-%m-%d %H:%M"),
        }
