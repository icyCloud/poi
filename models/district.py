# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME
from tornado.util import ObjectDict

import cache

class DistrictModel(Base):

    __tablename__ = 'district'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    MC_ALL_DISTRICT = __tablename__ + "mc_all_district"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    city_id = Column('cityId', INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    qunar_id = Column('qunarId', VARCHAR(50), nullable=False)
    elong_id = Column('elongId', VARCHAR(50), nullable=False)
    ctrip_id = Column('ctripId', INTEGER(unsigned=True), nullable=False)

    @classmethod
    @cache.mc(MC_ALL_DISTRICT)
    def get_all(self,session):
        return session.query(DistrictModel).all()

    @classmethod
    def get_by_ids(self, session, ids):
        return session.query(DistrictModel)\
                .filter(DistrictModel.id.in_(ids))\
                .all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                city_id=self.city_id,
                name=self.name,
                )
