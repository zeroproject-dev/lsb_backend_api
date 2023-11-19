from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer

from .video import TVIDEO
from .word import TWORD

from src.database.db import db


@dataclass
class TWORDVIDEO(db.Model):
    __tablename__ = "T_WORD_VIDEO"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(TWORD.id))
    video_id = Column(Integer, ForeignKey(TVIDEO.id))
