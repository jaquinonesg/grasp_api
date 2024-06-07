from pydantic import BaseModel


class ExampleRM(BaseModel):
    pk_example: str
    string_example: str
    string2_example: str


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str
