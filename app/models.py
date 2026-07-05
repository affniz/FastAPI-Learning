from .database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship,column_property
from sqlalchemy import ForeignKey,select
from datetime import datetime
from sqlalchemy import DateTime, func

class Vote(Base):
    __tablename__='votes'
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)

class Post(Base):
    __tablename__='posts'

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=False)
    content:Mapped[str] = mapped_column(nullable=False)
    published:Mapped[bool] = mapped_column(default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)

    owner = relationship("User")
    
class User(Base):
    __tablename__='users'
    id:Mapped[int] = mapped_column(primary_key=True,nullable=False)
    email:Mapped[str] = mapped_column(nullable=False,unique=True)
    password:Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
    )


