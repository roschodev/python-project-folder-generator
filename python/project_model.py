from pydantic import BaseModel

class Project(BaseModel):
    code: int
    location: str
    name: str
    client: str