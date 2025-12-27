from sqlmodel import SQLModel,Field,JSON
from datetime import datetime,timezone

class Articles(SQLModel,table=True):
    Id:int | None=Field(default=None,primary_key=True)
    Topic:str=Field(index=True,unique=True)
    Title:str=Field(index=True)
    Text:list[str]=Field(sa_type=JSON)
    Created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))