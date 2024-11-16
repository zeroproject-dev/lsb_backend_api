from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Enum, Integer, String, TIMESTAMP, Float

from ..database.db import db


class TVIDEO(db.Model):
    __tablename__ = "T_VIDEO"

    id = Column(Integer, primary_key=True)
    points = Column(String(255))
    path = Column(String(255), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("T_USER.id"), nullable=False)
    preview = Column(String(255))
    duration = Column(Float)
    bucket = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    uploaded_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    state = Column(Enum("active", "inactive"), server_default=text("'active'"))

    def from_json(self, json):
        self.path = json["path"]
        self.uploaded_by = json["uploaded_by"]
        self.preview = json["preview"]
        self.uploaded_date = json["uploaded_date"]
        self.state = "active" if self.state is None else self.state

    def to_json(self):
        json = {}
        json["id"] = self.id
        json["path"] = self.path
        json["uploaded_by"] = self.uploaded_by
        json["preview"] = self.preview
        json["bucket"] = self.bucket
        json["region"] = self.region
        json["uploaded_date"] = self.uploaded_date
        json["state"] = self.state

        return json
