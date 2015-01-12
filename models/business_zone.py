# -*- coding: utf-8 -*-

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT, DOUBLE, TEXT
from tornado.util import ObjectDict

class BusinessZoneModel(Base):

    __tablename__ = 'businessZone'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    elong_id = Column("elongId", VARCHAR(50), default='0')
    city_id = Column("cityId", INTEGER, default=0)
    name = Column(VARCHAR(50))
    type = Column(TINYINT(3))


    @classmethod
    def get_by_ids(self, session, ids):
        return session.query(BusinessZoneModel)\
                .filter(BusinessZoneModel.id.in_(ids))\
                .all()

    def todict(self):
        return ObjectDict(
                id=self.id,
                elong_id=self.elong_id,
                city_id=self.city_id,
                name=self.name,
                )
