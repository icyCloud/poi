# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from tornado.util import ObjectDict
import cache
from models import Base


class ProvinceModel(Base):
    __tablename__ = 'province'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    py_name = Column('pyName', VARCHAR(50), nullable=False)
    taobao_id = Column('taobaoId', VARCHAR(50), nullable=False)

    MC_ALL_PROVINCE = __tablename__ + "mc_all_province"
    MC_ALL_PROVINCE_DICT = __tablename__ + "mc_all_province_dict"

    @classmethod
    @cache.mc(MC_ALL_PROVINCE)
    def get_all(cls, session):
        return session.query(ProvinceModel).all()

    @classmethod
    @cache.mc(MC_ALL_PROVINCE_DICT)
    def get_all_dicts(cls, session):
        provinces = cls.get_all(session)
        return [province.todict() for province in provinces]

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(ProvinceModel) \
            .filter(ProvinceModel.id.in_(ids)) \
            .all()

    def todict(self):
        return ObjectDict(
            id=self.id,
            name=self.name,
        )

