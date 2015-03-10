# -*- coding: utf-8 -*-

import time

from models import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIT, INTEGER, VARCHAR, DATETIME, TIMESTAMP, TINYINT, DOUBLE, TEXT
from tornado.util import ObjectDict
from tools.utils import exe_time
from tools.log import Log

class HotelModel(Base):

    __tablename__ = 'hotel'
    __table_args__ = {
        'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    zipcode = Column("zipCode", VARCHAR(10), default="0")
    star = Column(TINYINT(3, unsigned=True), nullable=False)
    phone = Column(VARCHAR(100))
    fax = Column(VARCHAR(100))
    establishment_date = Column("establishmentDate", VARCHAR(15))
    renovation_date = Column("renovationDate", VARCHAR(15))
    is_economic = Column("isEconomic", BIT(1), default=0, nullable=False)
    is_apartment = Column("isApartment", BIT(1), default=0, nullable=False)
    glog = Column("gLog", DOUBLE, default=0, nullable=False)
    glat = Column("gLat", DOUBLE, default=0, nullable=False)
    blog = Column("bLog", DOUBLE, default=0, nullable=False)
    blat = Column("bLat", DOUBLE, default=0, nullable=False)
    city_id = Column('cityId', INTEGER(unsigned=True), nullable=False)
    district_id = Column('districtId', INTEGER(unsigned=True), nullable=False)
    facilities = Column(VARCHAR(200), nullable=False)
    business_zone = Column("businessZone", INTEGER(unsigned=True), default=0, nullable=False)
    foreigner_checkin = Column("foreignerCheckIn", BIT(1), default=0, nullable=False)
    require_idcard = Column("requireIdCard", BIT(1), default=0, nullable=False)
    intro = Column(TEXT)
    description = Column(TEXT)
    traffic = Column(TEXT)
    is_valid = Column('isValid', BIT, nullable=False)
    is_online = Column('isOnline', BIT, nullable=False)

    @classmethod
    def get_by_id(cls, session, id, need_online=False):
        query = session.query(HotelModel)\
                .filter(HotelModel.id == id)\
                .filter(HotelModel.is_valid == 1)
        if need_online:
            query = query.filter(HotelModel.is_online == 1)
        return query.first()


    @classmethod
    def get_by_ids(cls, session, ids, need_online=False):
        query = session.query(HotelModel)\
                .filter(HotelModel.id.in_(ids))\
                .filter(HotelModel.is_valid == 1)
        if need_online:
            query = query.filter(HotelModel.is_online == 1)
        return query.all()

    @classmethod
    def query(cls, session, name=None, star=None, city_id=None, district_id=None, start=0, limit=10, filter_ids=None, within_ids=None, count_total=True):
        query = session.query(HotelModel)\
                .filter(HotelModel.is_valid == 1)
        if within_ids:
            query = query.filter(HotelModel.id.in_(within_ids))
        if filter_ids:
            query = query.filter(~HotelModel.id.in_(filter_ids))
        if name:
            query = query.filter(HotelModel.name.like(u'%{}%'.format(name)))
        if star:
            query = query.filter(HotelModel.star == star)
        if city_id:
            query = query.filter(HotelModel.city_id == city_id)
        if district_id:
            query = query.filter(HotelModel.district_id == district_id)

        Log.info("=" * 30)
        t0 = time.time()
        r = query.offset(start).limit(limit).all()
        t1 = time.time()
        if count_total:
            total = query.count()
            return r, total
            t2 = time.time()
            Log.info(">>HotelSearch query cost:{} query total cost:{}".format(t1 - t0, t2-t1))
        else:
            return r

    @classmethod
    def new(cls, session,
            name, star, facilities, blog, blat, glog, glat, city_id, district_id, address, bussiness_zone, phone, traffic, description, require_idcard, is_online):
        hotel = HotelModel(name=name, star=star, facilities=facilities, blog=blog, blat=blat, glog=glog, glat=glat, city_id=city_id, district_id=district_id, address=address, business_zone=business_zone, phone=phone, traffic=traffic, description=description, require_idcard=require_idcard, is_online=isOnline)
        session.add(hotel)
        session.commit()
        return hotel

    @classmethod
    def update(cls, session, hotel_id,
            name, star, facilities, blog, blat, glog, glat, city_id, district_id, address, bussiness_zone, phone, traffic, description, require_idcard, is_online):
        hotel = cls.get_by_id(session, hotel_id)
        hotel.name = name
        hotel.star = star
        hotel.facilities = facilities
        hotel.blog = blog
        hotel.blat = blat
        hotel.glog = glog
        hotel.glat = glat
        hotel.city_id = city_id
        hotel.district_id= district_id
        hotel.address = address
        hotel.bussiness_zone = business_zone
        hotel.phone = phone
        hotel.traffic = traffic
        hotel.description = description
        hotel.require_idcard = require_idcard
        hotel.is_online = is_online
        session.commit()

        return hotel


    def todict(self):
        return dict(
                id=self.id,
                name=self.name,
                address=self.address,
                zipcode=self.zipcode,
                star=self.star,
                phone=self.phone,
                fax=self.fax,
                establishment_date=self.establishment_date,
                renovation_date=self.renovation_date,
                is_economic=self.is_economic,
                is_apartment=self.is_apartment,
                glog=self.glog,
                glat=self.glat,
                blog=self.blog,
                blat=self.blat,
                city_id=self.city_id,
                district_id=self.district_id,
                facilities=self.facilities,
                business_zone=self.business_zone,
                foreigner_checkin=self.foreigner_checkin,
                require_idcard=self.require_idcard,
                intro=self.intro,
                description=self.description,
                is_valid=self.is_valid,
                is_online=self.is_online,
                traffic=self.traffic,
                )
