# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME
from tornado.util import ObjectDict

import cache

class CityModel(Base):

    __tablename__ = 'city'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    qunar_id = Column('qunarId', VARCHAR(50), nullable=False)
    elong_id = Column('elongId', VARCHAR(50), nullable=False)
    ctrip_id = Column('ctripId', INTEGER(unsigned=True), nullable=False)
    prov_id = Column('provId', INTEGER(unsigned=True), nullable=False)

    MC_ALL_CITY = __tablename__ + "mc_all_city"

    @classmethod
    @cache.mc(MC_ALL_CITY)
    def get_all(self,session):
        return session.query(CityModel).all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                name=self.name,
                )
