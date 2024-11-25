from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.expression import false, true

from .orm.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String(254))
    password: Mapped[str] = mapped_column(String(128))

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))

    is_active: Mapped[bool] = mapped_column(server_default=true())
    is_staff: Mapped[bool] = mapped_column(server_default=false())
    is_superuser: Mapped[bool] = mapped_column(server_default=false())

    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(server_default=func.now())
