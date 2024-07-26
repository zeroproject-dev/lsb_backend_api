from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import Enum, Integer, String

from database.db import db
from models.role import TROLE
from utils.passwords import check_password


class TUSER(db.Model):
    __tablename__ = "T_USER"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    first_surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)
    second_name = Column(String(255))
    second_surname = Column(String(255))
    state = Column(Enum("active", "inactive"), server_default=text("'active'"))
    role_id = Column(Integer, ForeignKey(TROLE.id))

    def from_json(self, json):
        self.first_name = json["first_name"]
        self.first_surname = json["first_surname"]
        self.email = json["email"]
        self.password = json["password"] if json.get("password") is not None else ""
        self.second_name = (
            json["second_name"] if json.get("second_name") is not None else ""
        )
        self.second_surname = json["second_surname"]
        self.role_id = json["role"]
        self.state = "active" if self.state is None else self.state

        return self

    def to_json(self):
        json = {}
        json["id"] = self.id
        json["first_name"] = self.first_name
        json["first_surname"] = self.first_surname
        json["email"] = self.email
        json["password"] = self.password
        json["second_name"] = self.second_name
        json["second_surname"] = self.second_surname
        json["role"] = self.role_id
        json["state"] = self.state

        return json

    def is_correct_password(self, password):
        return check_password(self.password, password)
