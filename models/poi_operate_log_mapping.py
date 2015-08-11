# -*- coding: utf-8 -*-
__author__ = 'jiangfuqiang'

from models import Base
from sqlalchemy import Column, or_,and_
from sqlalchemy.dialects.mysql import BIT,INTEGER,VARCHAR,DATETIME,TIMESTAMP,TINYINT,BIGINT
from tornado.util import ObjectDict
import datetime

class PoiOperateLogModel(Base):
    __tablename__ = 'poi_operate_log'
    __table_args__ = {
        'mysql_charset':'utf8', 'mysql_engine':'InnoDB'
    }

    STATUS = ObjectDict({
        'init':0,
        'wait_first_valid':1,
        'wait_second_valid':2,
        'valid_complete':3
    })

    id = Column(BIGINT(unsigned=True),primary_key=True,autoincrement=True)
    ota_id = Column('ota_id',INTEGER(unsigned=True),nullable=False)
    hotel_id = Column('hotel_id',VARCHAR,nullable=False)
    hotel_name = Column('hotel_name',VARCHAR,nullable=False)
    motivation = Column('motivation', INTEGER(unsigned=True), nullable=False)
    operate_content = Column('operate_content', VARCHAR, nullable=False)
    operator = Column('operator', VARCHAR, nullable=False)
    module = Column('module',INTEGER(unsigned=True), nullable=False)
    poi_hotel_id = Column('poi_hotel_id', BIGINT(unsigned=True), nullable=False)
    poi_roomtype_id = Column('poi_roomtype_id',BIGINT(unsigned=True))
    tsupdate = Column('tsupdate', TIMESTAMP, nullable=False)

    @classmethod
    def get_poilog(cls,session,otaId=None,hotelName=None,module=None,motivation=None,operator=None,startDate=None,endDate=None,start=0,limit=10):
        query = session.query(PoiOperateLogModel)


        if otaId is not None:
            query = query.filter(PoiOperateLogModel.ota_id==otaId)
        if hotelName:
            query = query.filter(PoiOperateLogModel.hotel_name.like(u'%{}%'.format(hotelName)))
        if module:
            query = query.filter(PoiOperateLogModel.module==module)
        if motivation:
            query = query.filter(PoiOperateLogModel.motivation == motivation)
        if operator:
            query = query.filter(PoiOperateLogModel.operator == operator)
        if startDate:
            sd = datetime.datetime.strptime(startDate,'%Y-%m-%d %H:%M:%S')
            ed = datetime.datetime.strptime(endDate,'%Y-%m-%d %H:%M:%S')
            query = query.filter(PoiOperateLogModel.tsupdate.between(sd,ed))
        data = query.order_by(PoiOperateLogModel.id.desc()).offset(start).limit(limit).all()
        total = query.count()
        return data,total

    @classmethod
    def record_log(cls,session,otaId=None,hotelName=None,module=None,motivation=None,operator=None,operate_content = None,poi_hotel_id=None,poi_roomtype_id=None,hotel_id=None):
        model = PoiOperateLogModel()
        model.ota_id = otaId
        model.hotel_name = hotelName
        model.module = module
        model.motivation = motivation
        model.operator = operator
        model.operate_content = operate_content
        model.poi_hotel_id = poi_hotel_id
        model.poi_roomtype_id = poi_roomtype_id
        model.hotel_id = hotel_id
        session.add(model)
        session.flush()
        session.commit()

    def todict(self):
        return ObjectDict(
            id=self.id,
            otaId=self.ota_id,
            hotelId = self.hotel_id,
            hotelName = self.hotel_name,
            motivation=self.motivation,
            module=self.module,
            operator=self.operator,
            operateContent=self.operate_content,
            poiHotelId=self.poi_hotel_id,
            poiRoomTypeId=self.poi_roomtype_id,
            tsupdate=self.tsupdate
        )