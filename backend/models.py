from datetime import datetime,timezone
from sqlmodel import SQLModel,Field,JSON


class Articles(SQLModel,table=True):
    Id:int | None=Field(default=None,primary_key=True)
    Topic:str=Field(index=True,unique=True)
    Title:str=Field(index=True)
    Text:str=Field(sa_type=JSON)
    Sources_used:list[str]=Field(sa_type=JSON)
    Created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))