from sqlalchemy.orm import relationship, mapped_column, Mapped


from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    baskets: Mapped[list["Baskets"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"
