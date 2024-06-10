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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "attributes": {"key": "value"},
                    "data": "eyJzZXJpYWwiOiAiNzUyODQyMzg3NzM1IiwgImFwcGxpY2F0aW9uIjogMjAsICJUaW1lIjogIjIwMjQtMDYtMDdUMTY6MTg6MjAuOTU0MjEyIiwgIlR5cGUiOiAieGtndyIsICJkZXZpY2UiOiAiVGVzdERldmljZSIsICJ2MCI6IDI0NDEzOCwgInYxIjogMC4xMSwgInYyIjogMC40OCwgInYzIjogMC4yLCAidjQiOiAxLCAidjUiOiAwLjE2LCAidjYiOiAwLCAidjciOiA3NTU1NCwgInY4IjogMC45MywgInY5IjogMzY2OTczNzIsICJ2MTAiOiAxLCAidjExIjogMSwgInYxMiI6IDIuMTMsICJ2MTMiOiAwLCAidjE0IjogMC45NCwgInYxNSI6IDYyODQ1LCAidjE2IjogOTQ2MTUxLCAidjE3IjogNTAzNTMsICJ2MTgiOiAxLjc3fQ==",
                    "messageId": "2070443601311540",
                    "message_id": "2070443601311540",
                    "publishTime": "2021-02-26T19:13:55.749Z",
                    "publish_time": "2021-02-26T19:13:55.749Z",
                }
            ]
        }
    }


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
