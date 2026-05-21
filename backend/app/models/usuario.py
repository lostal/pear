from sqlmodel import Field, Relationship, SQLModel

class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False, index=True, max_length=100)
    password_hash: str = Field(nullable=False, max_length=255)
    role: str = Field(default="user", max_length=20)
    cart_items: list["CartItem"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})
