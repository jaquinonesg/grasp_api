from datetime import datetime

from pydantic import BaseModel, validator


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class MessageAttributes(BaseModel):
    key: str


class InnerMessage(BaseModel):
    attributes: MessageAttributes
    data: str
    messageId: str
    message_id: str
    publishTime: str
    publish_time: str


class PubSubMessage(BaseModel):
    # Handles input from Google Pub/Sub
    message: InnerMessage
    subscription: str


class SensorDataIn(BaseModel):
    # Handles data after cleaning the Pub/Sub payload
    sensor_id: str
    dwell_time: str
    time: datetime

    @validator("time", pre=True)
    def parse_time(cls, value):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("time must be in ISO8601 format")


class SensorDataOut(BaseModel):
    sensor_id: str
    dwell_time: str
    time: datetime

    class Config:
        orm_mode = True
