# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME
from tornado.util import ObjectDict

import cache
from tools.utils import exe_time

class DistrictModel(Base):

    __tablename__ = 'district'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    MC_ALL_DISTRICT = __tablename__ + "mc_all_district"
    MC_ALL_DISTRICT_DICT = __tablename__ + "mc_all_district_dict"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    city_id = Column('cityId', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    qunar_id = Column('qunarId', VARCHAR(50), nullable=False)
    elong_id = Column('elongId', VARCHAR(50), nullable=False)
    ctrip_id = Column('ctripId', INTEGER(unsigned=True), nullable=False)

    @classmethod
    @cache.mc(MC_ALL_DISTRICT)
    def get_all(cls, session):
        return session.query(DistrictModel).all()

    @classmethod
    @cache.mc(MC_ALL_DISTRICT_DICT)
    def get_all_dicts(cls, session):
        districts = cls.get_all(session)
        return [district.todict() for district in districts]

    @classmethod
    def get_by_ids(cls, session, ids):
        return session.query(DistrictModel)\
                .filter(DistrictModel.id.in_(ids))\
                .all()

    @classmethod
    def get_by_city_id(cls, session, city_id):
        return session.query(DistrictModel)\
                .filter(DistrictModel.city_id == city_id)\
                .all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                city_id=self.city_id,
                name=self.name,
                )

    def tojson(self):
        return dict(
                id=self.id,
                city_id=self.city_id,
                name=self.name,
                )
