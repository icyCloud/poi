# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TINYINT
from tornado.util import ObjectDict

import cache

class FacilityModel(Base):

    __tablename__ = 'facility'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50))
    type = Column(TINYINT(3, unsigned=True))
    hotel_facility_type = Column("hotelFacilityType", TINYINT(3, unsigned=True))

    MC_ALL_FACILITY = __tablename__ + "mc_all_facility"
    MC_ALL_FACILITY_TYPE_IS_ROOM  = __tablename__ + "mc_all_facility_type_is_room"

    @classmethod
    @cache.mc(MC_ALL_FACILITY)
    def get_all(self, session):
        return session.query(FacilityModel).all()

    @classmethod
    @cache.mc(MC_ALL_FACILITY_TYPE_IS_ROOM)
    def get_all_type_is_room(self, session):
        return session.query(FacilityModel)\
                .filter(FacilityModel.type == 1)\
                .all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                name=self.name,
                type=self.type,
                hotel_facility_type=self.hotel_facility_type)
