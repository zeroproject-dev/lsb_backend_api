from sqlalchemy import Column, Enum, ForeignKeyConstraint, Index, Integer, JSON, LargeBinary, String, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TPERMISSION(Base):
    __tablename__ = 'T_PERMISSION'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))

    T_ROLE_PERMISSION = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.permission_id]', back_populates='permission')
    T_ROLE_PERMISSION_ = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.permission_id]', back_populates='permission_')
    T_ROLE_PERMISSION1 = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.permission_id]', back_populates='permission1')
    T_ROLE_PERMISSION2 = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.permission_id]', back_populates='permission2')


class TROLE(Base):
    __tablename__ = 'T_ROLE'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))

    T_ROLE_PERMISSION = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.role_id]', back_populates='role')
    T_ROLE_PERMISSION_ = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.role_id]', back_populates='role_')
    T_ROLE_PERMISSION1 = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.role_id]', back_populates='role1')
    T_ROLE_PERMISSION2 = relationship('TROLEPERMISSION', foreign_keys='[TROLEPERMISSION.role_id]', back_populates='role2')
    T_USER = relationship('TUSER', foreign_keys='[TUSER.role_id]', back_populates='role')
    T_USER_ = relationship('TUSER', foreign_keys='[TUSER.role_id]', back_populates='role_')
    T_USER1 = relationship('TUSER', foreign_keys='[TUSER.role_id]', back_populates='role1')
    T_USER2 = relationship('TUSER', foreign_keys='[TUSER.role_id]', back_populates='role2')


class TWORD(Base):
    __tablename__ = 'T_WORD'

    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=False)
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))

    T_WORD_VIDEO = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.word_id]', back_populates='word')
    T_WORD_VIDEO_ = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.word_id]', back_populates='word_')
    T_WORD_VIDEO1 = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.word_id]', back_populates='word1')
    T_WORD_VIDEO2 = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.word_id]', back_populates='word2')


class TROLEPERMISSION(Base):
    __tablename__ = 'T_ROLE_PERMISSION'
    __table_args__ = (
        ForeignKeyConstraint(['permission_id'], ['T_PERMISSION.id'], name='T_ROLE_PERMISSION_ibfk_1'),
        ForeignKeyConstraint(['permission_id'], ['T_PERMISSION.id'], name='T_ROLE_PERMISSION_ibfk_3'),
        ForeignKeyConstraint(['permission_id'], ['T_PERMISSION.id'], name='T_ROLE_PERMISSION_ibfk_5'),
        ForeignKeyConstraint(['permission_id'], ['T_PERMISSION.id'], name='T_ROLE_PERMISSION_ibfk_7'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_ROLE_PERMISSION_ibfk_2'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_ROLE_PERMISSION_ibfk_8'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_ROLE_PERMISSION_ibfk_6'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_ROLE_PERMISSION_ibfk_4'),
        Index('permission_id', 'permission_id'),
        Index('role_id', 'role_id')
    )

    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer)
    role_id = Column(Integer)

    permission = relationship('TPERMISSION', foreign_keys=[permission_id], back_populates='T_ROLE_PERMISSION')
    permission_ = relationship('TPERMISSION', foreign_keys=[permission_id], back_populates='T_ROLE_PERMISSION_')
    permission1 = relationship('TPERMISSION', foreign_keys=[permission_id], back_populates='T_ROLE_PERMISSION1')
    permission2 = relationship('TPERMISSION', foreign_keys=[permission_id], back_populates='T_ROLE_PERMISSION2')
    role = relationship('TROLE', foreign_keys=[role_id], back_populates='T_ROLE_PERMISSION')
    role_ = relationship('TROLE', foreign_keys=[role_id], back_populates='T_ROLE_PERMISSION_')
    role1 = relationship('TROLE', foreign_keys=[role_id], back_populates='T_ROLE_PERMISSION1')
    role2 = relationship('TROLE', foreign_keys=[role_id], back_populates='T_ROLE_PERMISSION2')


class TUSER(Base):
    __tablename__ = 'T_USER'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_USER_ibfk_1'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_USER_ibfk_3'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_USER_ibfk_4'),
        ForeignKeyConstraint(['role_id'], ['T_ROLE.id'], name='T_USER_ibfk_2'),
        Index('role_id', 'role_id')
    )

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    first_surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    second_name = Column(String(255))
    second_surname = Column(String(255))
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))
    role_id = Column(Integer)

    role = relationship('TROLE', foreign_keys=[role_id], back_populates='T_USER')
    role_ = relationship('TROLE', foreign_keys=[role_id], back_populates='T_USER_')
    role1 = relationship('TROLE', foreign_keys=[role_id], back_populates='T_USER1')
    role2 = relationship('TROLE', foreign_keys=[role_id], back_populates='T_USER2')
    T_AUDIT_LOG = relationship('TAUDITLOG', foreign_keys='[TAUDITLOG.performed_by]', back_populates='T_USER')
    T_AUDIT_LOG_ = relationship('TAUDITLOG', foreign_keys='[TAUDITLOG.performed_by]', back_populates='T_USER_')
    T_AUDIT_LOG1 = relationship('TAUDITLOG', foreign_keys='[TAUDITLOG.performed_by]', back_populates='T_USER1')
    T_AUDIT_LOG2 = relationship('TAUDITLOG', foreign_keys='[TAUDITLOG.performed_by]', back_populates='T_USER2')
    T_VIDEO = relationship('TVIDEO', foreign_keys='[TVIDEO.uploaded_by]', back_populates='T_USER')
    T_VIDEO_ = relationship('TVIDEO', foreign_keys='[TVIDEO.uploaded_by]', back_populates='T_USER_')
    T_VIDEO1 = relationship('TVIDEO', foreign_keys='[TVIDEO.uploaded_by]', back_populates='T_USER1')
    T_VIDEO2 = relationship('TVIDEO', foreign_keys='[TVIDEO.uploaded_by]', back_populates='T_USER2')


class TAUDITLOG(Base):
    __tablename__ = 'T_AUDIT_LOG'
    __table_args__ = (
        ForeignKeyConstraint(['performed_by'], ['T_USER.id'], name='T_AUDIT_LOG_ibfk_1'),
        ForeignKeyConstraint(['performed_by'], ['T_USER.id'], name='T_AUDIT_LOG_ibfk_2'),
        ForeignKeyConstraint(['performed_by'], ['T_USER.id'], name='T_AUDIT_LOG_ibfk_3'),
        ForeignKeyConstraint(['performed_by'], ['T_USER.id'], name='T_AUDIT_LOG_ibfk_4'),
        Index('performed_by', 'performed_by')
    )

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(255))
    entity_id = Column(Integer)
    action = Column(Enum('insert', 'update', 'delete'))
    changed_columns = Column(String(255))
    changed_data = Column(JSON)
    timestamp = Column(TIMESTAMP)
    performed_by = Column(Integer)

    T_USER = relationship('TUSER', foreign_keys=[performed_by], back_populates='T_AUDIT_LOG')
    T_USER_ = relationship('TUSER', foreign_keys=[performed_by], back_populates='T_AUDIT_LOG_')
    T_USER1 = relationship('TUSER', foreign_keys=[performed_by], back_populates='T_AUDIT_LOG1')
    T_USER2 = relationship('TUSER', foreign_keys=[performed_by], back_populates='T_AUDIT_LOG2')


class TVIDEO(Base):
    __tablename__ = 'T_VIDEO'
    __table_args__ = (
        ForeignKeyConstraint(['uploaded_by'], ['T_USER.id'], name='T_VIDEO_ibfk_1'),
        ForeignKeyConstraint(['uploaded_by'], ['T_USER.id'], name='T_VIDEO_ibfk_4'),
        ForeignKeyConstraint(['uploaded_by'], ['T_USER.id'], name='T_VIDEO_ibfk_2'),
        ForeignKeyConstraint(['uploaded_by'], ['T_USER.id'], name='T_VIDEO_ibfk_3'),
        Index('uploaded_by', 'uploaded_by')
    )

    id = Column(Integer, primary_key=True)
    path = Column(String(255), nullable=False)
    uploaded_by = Column(Integer, nullable=False)
    preview = Column(LargeBinary)
    uploaded_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    state = Column(Enum('active', 'inactive'), server_default=text("'active'"))

    T_USER = relationship('TUSER', foreign_keys=[uploaded_by], back_populates='T_VIDEO')
    T_USER_ = relationship('TUSER', foreign_keys=[uploaded_by], back_populates='T_VIDEO_')
    T_USER1 = relationship('TUSER', foreign_keys=[uploaded_by], back_populates='T_VIDEO1')
    T_USER2 = relationship('TUSER', foreign_keys=[uploaded_by], back_populates='T_VIDEO2')
    T_WORD_VIDEO = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.video_id]', back_populates='video')
    T_WORD_VIDEO_ = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.video_id]', back_populates='video_')
    T_WORD_VIDEO1 = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.video_id]', back_populates='video1')
    T_WORD_VIDEO2 = relationship('TWORDVIDEO', foreign_keys='[TWORDVIDEO.video_id]', back_populates='video2')


class TWORDVIDEO(Base):
    __tablename__ = 'T_WORD_VIDEO'
    __table_args__ = (
        ForeignKeyConstraint(['video_id'], ['T_VIDEO.id'], name='T_WORD_VIDEO_ibfk_4'),
        ForeignKeyConstraint(['video_id'], ['T_VIDEO.id'], name='T_WORD_VIDEO_ibfk_6'),
        ForeignKeyConstraint(['video_id'], ['T_VIDEO.id'], name='T_WORD_VIDEO_ibfk_2'),
        ForeignKeyConstraint(['video_id'], ['T_VIDEO.id'], name='T_WORD_VIDEO_ibfk_8'),
        ForeignKeyConstraint(['word_id'], ['T_WORD.id'], name='T_WORD_VIDEO_ibfk_3'),
        ForeignKeyConstraint(['word_id'], ['T_WORD.id'], name='T_WORD_VIDEO_ibfk_5'),
        ForeignKeyConstraint(['word_id'], ['T_WORD.id'], name='T_WORD_VIDEO_ibfk_7'),
        ForeignKeyConstraint(['word_id'], ['T_WORD.id'], name='T_WORD_VIDEO_ibfk_1'),
        Index('video_id', 'video_id'),
        Index('word_id', 'word_id')
    )

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer)
    video_id = Column(Integer)

    video = relationship('TVIDEO', foreign_keys=[video_id], back_populates='T_WORD_VIDEO')
    video_ = relationship('TVIDEO', foreign_keys=[video_id], back_populates='T_WORD_VIDEO_')
    video1 = relationship('TVIDEO', foreign_keys=[video_id], back_populates='T_WORD_VIDEO1')
    video2 = relationship('TVIDEO', foreign_keys=[video_id], back_populates='T_WORD_VIDEO2')
    word = relationship('TWORD', foreign_keys=[word_id], back_populates='T_WORD_VIDEO')
    word_ = relationship('TWORD', foreign_keys=[word_id], back_populates='T_WORD_VIDEO_')
    word1 = relationship('TWORD', foreign_keys=[word_id], back_populates='T_WORD_VIDEO1')
    word2 = relationship('TWORD', foreign_keys=[word_id], back_populates='T_WORD_VIDEO2')
