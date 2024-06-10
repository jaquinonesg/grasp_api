from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def to_dict(self, exclude_fields: list | None = None):
        return {
            field.name: getattr(self, field.name)
            for field in self.__table__.c
            if not exclude_fields or field.name not in exclude_fields
        }


class SensorData(Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    sensor_id: Mapped[str | None] = mapped_column(String(10))
    dwell_time: Mapped[str | None] = mapped_column(String(10))
    time: Mapped[datetime | None] = mapped_column(DateTime)
