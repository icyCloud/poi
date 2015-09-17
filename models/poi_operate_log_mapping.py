# -*- coding: utf-8 -*-
__author__ = 'jiangfuqiang'

from models import Base
from sqlalchemy import Column, or_,and_
from sqlalchemy.dialects.mysql import BIT,INTEGER,VARCHAR,DATETIME,TIMESTAMP,TINYINT,BIGINT
from tornado.util import ObjectDict
import datetime
import json
from config import searchapi
import traceback
import urllib2
import urllib
from tools.log import Log, log_request

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

        tsearchApi = searchapi
        tsearchApi += '?start=' + str(start) + "&limit=" + str(limit)
        if otaId:
            tsearchApi += '&chain_id=' + str(otaId)
        if hotelName:
            tsearchApi += "&"+urllib.urlencode({'hotel_name':hotelName})
            # tsearchApi += "&hotel_name=" + hotelName.encode('utf-8')
        if module:
            tsearchApi += "&module=" + str(module)
        if motivation:
            tsearchApi += "&motivation=" + str(motivation)
        if operator:
            tsearchApi += '&operator=' + operator
        if startDate:
            tsearchApi += '&from_date=' + startDate
        if endDate:
            tsearchApi += '&to_date=' + endDate
        Log.info('tsearchapi==' + tsearchApi)
        total = 0
        logs = []
        try:
            headers = { 'Content-Type' : 'application/json;charset=utf-8' }
            req = urllib2.Request(tsearchApi, headers=headers)
            response = urllib2.urlopen(req)
            data = response.read()
            jon = json.loads(data)
            if int(jon['errcode']) == 0:
                result = jon['result']
                total = result['count']
                rows = result['rows']

                if len(rows) > 0:
                    for row in rows:
                        row['operateContent'] = row['content']
                        row['otaId'] = row['chain_id']
                        row['hotelName'] = row['hotel_name']
                        logs.append(row)
        except Exception,e:
            traceback.print_exc()
        finally:
            return logs,total




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